package proj

import java.time.{LocalDate, Period}

import proj.Constants.reddit_schema
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{DataTypes, StructType}

import org.apache.spark.rdd.RDD

//elastic search imports
import com.typesafe.config.ConfigFactory
import org.elasticsearch.hadoop.cfg.ConfigurationOptions

//redis connectors
import com.redislabs.provider.redis._

object StreamsProcessor {
  def main(args: Array[String]): Unit = {
    new StreamsProcessor("localhost:9092").process()
  }
}

class StreamsProcessor(brokers: String) {

  private val config = ConfigFactory.load()

  private val master = config.getString("spark.master")

  private val pathToJSONResource = config.getString("spark.json.resource.path")

  private val elasticsearchUser = config.getString("spark.elasticsearch.username")
  private val elasticsearchPass = config.getString("spark.elasticsearch.password")
  private val elasticsearchHost = config.getString("spark.elasticsearch.host")
  private val elasticsearchPort = config.getString("spark.elasticsearch.port")

  private val outputMode = config.getString("spark.elasticsearch.output.mode")
  private val destination = config.getString("spark.elasticsearch.data.source")
  private val checkpointLocation = config.getString("spark.elasticsearch.checkpoint.location")
  private val docType = config.getString("spark.elasticsearch.doc.type")
  //private val indexAndDocType = s"$index/$docType"

  def process(): Unit = {

    val spark = SparkSession.builder()
      .config(ConfigurationOptions.ES_NET_HTTP_AUTH_USER, elasticsearchUser)
      .config(ConfigurationOptions.ES_NET_HTTP_AUTH_PASS, elasticsearchPass)
      .config(ConfigurationOptions.ES_NODES, elasticsearchHost)
      .config(ConfigurationOptions.ES_PORT, elasticsearchPort)
      .appName("proj")
      .master(master)
      .getOrCreate()

    import spark.implicits._

    val stream_df = spark.readStream
                          .format("kafka")
                          .option("kafka.bootstrap.servers", brokers)
                          .option("subscribe", "persons-avro")
                          .load()


    //val query_1= stream_df.writeStream
    //                     .outputMode("append")
    //                     .format("console")
    //                     .start()

    val df = stream_df.selectExpr("CAST(value as STRING)")


    val reddit_df = df.select(from_json('value, reddit_schema ) as 'reddit_comment)

    val query_2 = reddit_df.writeStream
                           .outputMode("append")
                           .format("console")
                           .start()


    //reddit_df.writeStream
    //       .outputMode(outputMode)
    //       .format(destination)
    //       .option("checkpointLocation", checkpointLocation)
    //       .start("reddit-comments/personal")
    //       .awaitTermination()


    reddit_df.printSchema()

    //query_1.awaitTermination()
    query_2.awaitTermination()
