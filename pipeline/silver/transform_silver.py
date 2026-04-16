import os
import time
import pandas as pd
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType, StringType 

load_dotenv()

MINIO_ENDPOINT = "http://localhost:9000"
MINIO_USER     = os.getenv("MINIO_ROOT_USER")
MINIO_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
SILVER_SCHEMA  = StructType([
        StructField("tournament_id",     IntegerType(), False),
        StructField("nb_players",        IntegerType(), False),
        StructField("buy_in",            FloatType(), False),
        StructField("estimate_dotation", FloatType(), False),
        StructField("total_dotation",    FloatType(), False),
        StructField("winner",            StringType(), False),
        StructField("winner_gain",       FloatType(), False), 
])

def create_spark_session() -> SparkSession:
    return (
        SparkSession.builder
        .appName("SpaceKO Silver Transform")
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262"
        )
        .config("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT)
        .config("spark.hadoop.fs.s3a.access.key", MINIO_USER)
        .config("spark.hadoop.fs.s3a.secret.key", MINIO_PASSWORD)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.sql.execution.arrow.pyspark.enabled", "false")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .getOrCreate()
    )

def read_bronze(spark: SparkSession):
    df = spark.read.parquet("s3a://bronze/tournaments/events.parquet")
    print(f"Events bronze load : {df.count()} lignes")
    df.printSchema()
    return df

def bank_robbery(token: int, dotation: float, rng: int) -> float:
    """Documentation officiel sur : https://www.winamax.fr/space-ko"""
    match token:
        case t if t <= 10:
            payouts = [(100, 100), (600, 10), (5100, 3), (17700, 2), (40000, 1), (100000, 0.4)]
        case 11:
            payouts = [(1000, 10), (6000, 3), (17000, 2), (40000, 1), (100000, 0.5)]
        case 12:
            payouts = [(6000, 3), (18000, 2), (40000, 1), (100000, 0.6)]
        case 13:
            payouts = [(16002, 2), (46660, 1), (100000, 0.7)]
        case 14:
            payouts = [(18570, 1.5), (53575, 1), (100000, 0.8)]

    for threshold, multiplier in payouts:
        if rng <= threshold:
            return dotation * multiplier

def checking_token(dotation:float, buy_in:float) -> int:
    """Documentation officiel sur : https://www.winamax.fr/space-ko """ 
    if dotation < buy_in * 0.6:
        return 1
    elif dotation < buy_in * 0.75:
        return 2
    elif dotation < buy_in:
        return 3
    elif dotation < buy_in * 1.5:
        return 4
    elif dotation < buy_in * 2.5:
        return 5
    elif dotation < buy_in * 5:
        return 6
    elif dotation < buy_in * 10:
        return 7
    elif dotation < buy_in * 20:
        return 8
    elif dotation < buy_in * 50:
        return 9
    elif dotation < 10000:
        return 10
    elif dotation < 100000:
        return 11
    elif dotation < 333333:
        return 12
    elif dotation < 500000:
        return 13
    else:
        return 14

def tournament_replayer(df):
    info = df[df["event_type"] == "tournament_info"].iloc[0]
    buy_in = info["buy_in"]
    nb_players = info["players"]
    tournament_id = info["tournament_id"]

    players = {}
    for i in range(1, int(nb_players) + 1):
        players[f"Player {i}"] = {
            "dotation" : buy_in / 2,
            "token_lvl": 1,
            "gain"     : 0,
            "kills"    : 0
        }
    
    bust_events = df[df["event_type"] == "bust_event"].sort_values("event_id")
    for _, event in bust_events.iterrows():
        winner = event["winner"]
        looser = event["looser"]
        rng    = int(event["rng"])

        money = bank_robbery(players[looser]["token_lvl"], players[looser]["dotation"], rng)
        split = round(money / 2, 2)

        players[winner]["dotation"] += split
        players[winner]["gain"] += split
        players[winner]["kills"] += 1
        players[winner]["token_lvl"] = checking_token(players[winner]["dotation"], buy_in)

    winner_event = df[df["event_type"] == "winner_event"].iloc[0]
    winner_name = winner_event["winner"]
    final_gain = bank_robbery(players[winner_name]["token_lvl"], players[winner_name]["dotation"], int(winner_event["rng"]))
    players[winner_name]["gain"] += final_gain
    total_dotation = round(sum(p["gain"] for p in players.values()), 2)

    return pd.DataFrame([{
        "tournament_id"     : int(tournament_id),
        "nb_players"        : int(nb_players),
        "buy_in"            : float(buy_in),
        "estimate_dotation" : round(buy_in / 2 * nb_players, 2),
        "total_dotation"    : total_dotation,
        "winner"            : winner_name,
        "winner_gain"       : round(players[winner_name]["gain"], 2)
    }])

def write_silver(spark: SparkSession, df):
    # silver_df = spark.createDataFrame(df, schema=SILVER_SCHEMA)
    df.write.mode("overwrite").parquet("s3a://silver/tournaments/results.parquet")
    print(f"Silver written : {df.count()} tournois")

# def main():
#     start = time.time()
#     spark = create_spark_session()
#     bronze_df = read_bronze(spark)

#     silver_df = (
#         bronze_df
#         .groupBy("tournament_id")
#         .applyInPandas(tournament_replayer, schema=SILVER_SCHEMA)
#     )

#     write_silver(spark, silver_df)
#     spark.stop()
#     end = time.time()
#     print(f"Le pipeline a mit {round(end - start, 2)} secondes.")
def main():
    start = time.time()
    spark = create_spark_session()
    bronze_df = read_bronze(spark)

    bronze_pandas = bronze_df.toPandas()

    results = []
    for _, group in bronze_pandas.groupby("tournament_id"):
        results.append(tournament_replayer(group))

    silver_pandas = pd.concat(results, ignore_index=True)
    silver_df = spark.createDataFrame(silver_pandas, schema=SILVER_SCHEMA)

    write_silver(spark, silver_df)
    spark.stop()
    end = time.time()
    print(f"Le pipeline a mit {round(end - start, 2)} secondes.")


if __name__ == "__main__":
    main()