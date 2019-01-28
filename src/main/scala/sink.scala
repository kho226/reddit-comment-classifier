package proj

import java.time.{LocalDate, Period}

import proj.Constants
import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.expressions.UserDefinedFunction
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{DataTypes, StructType}

//elastic search imports
import com.typesafe.config.ConfigFactory
import org.elasticsearch.hadoop.cfg.ConfigurationOptions


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
  private val index = config.getString("spark.elasticsearch.index")
  private val docType = config.getString("spark.elasticsearch.doc.type")
  private val indexAndDocType = s"$index/$docType"


  def process(): Unit = {

    val spark = SparkSession.builder()
      .config(ConfigurationOptions.ES_NET_HTTP_AUTH_USER, elasticsearchUser)
      .config(ConfigurationOptions.ES_NET_HTTP_AUTH_PASS, elasticsearchPass)
      .config(ConfigurationOptions.ES_NODES, elasticsearchHost)
      .config(ConfigurationOptions.ES_PORT, elasticsearchPort)
      .appName("proj")
      .master(master)
      .getOrCreate()


   val df = spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", brokers)
        .option("subscribe", "persons-avro")
        .load()


  val query = df.writeStream
        .outputMode("append")
        .format("console")
        .start()

  query.awaitTermination()

  }
