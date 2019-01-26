package proj

import java.time.{LocalDate, Period}

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{DataTypes, StructType}


object StreamsProcessor {
  def main(args: Array[String]): Unit = {
    new StreamsProcessor("localhost:9092").process()
  }
}

class StreamsProcessor(brokers: String) {

  def process(): Unit = {

    val spark = SparkSession.builder()
      .appName("proj")
      .master("local[*]")
      .getOrCreate()

    import spark.implicits._

    val inputDf = spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", brokers)
      .option("subscribe", "spark-test")
      .load()


    val jsonDf = inputDf.selectExpr("CAST(value AS STRING)")

    val struct = new StructType()
      .add("source", DataTypes.StringType)
      .add("last_price", DataTypes.StringType)
      .add("num_contracts", DataTypes.StringType)
      .add("date_time", DataTypes.StringType)
  
    val nestedDf = jsonDf.select(from_json($"value", struct).as("ticker"))

    val flattenedDf = nestedDf.selectExpr("ticker.last_price", "ticker.num_contracts", "ticker.date_time")

    val resDf = flattenedDf.select(
      concat($"date_time", lit(" "), $"num_contracts").as("key"),
      flattenedDf.col("last_price").cast(DataTypes.StringType).as("value"))

    val kafkaOutput = resDf.writeStream
      .format("kafka")
      .option("kafka.bootstrap.servers", brokers)
      .option("topic", "from-spark")
      .option("checkpointLocation", "/spark/checkpoints")
      .start()

    kafkaOutput.awaitTermination()

    }
}
