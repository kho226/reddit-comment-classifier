//Author: Kyle Ong
//Date: 02/02/2019
//Constans for trenddit spark structured streaming

package trenddit
import java.time.format.DateTimeFormatter
import org.apache.spark.sql.types.{DataTypes, StructType}

object Constants {
  val personsTopic = "persons"
  val personsAvroTopic = "persons-avro"
  val agesTopic = "ages"

  val dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSSZ")
  
  val reddit_schema = new StructType()
    .add("archived", DataTypes.BooleanType)
    .add("author", DataTypes.StringType)
    .add("author_created_utc", DataTypes.LongType)
    .add("author_flair_background_color", DataTypes.StringType)
    .add("author_flair_css_class", DataTypes.StringType)
    .add("author_flair_template_id", DataTypes.StringType)
    .add("author_flair_text", DataTypes.StringType)
    .add("author_flair_text_color", DataTypes.StringType)
    .add("author_flair_type", DataTypes.StringType)
    .add("author_fullname", DataTypes.StringType)
    .add("author_patreon_flair", DataTypes.BooleanType)
    .add("body", DataTypes.StringType)
    .add("can_gild", DataTypes.BooleanType)
    .add("can_mod_post", DataTypes.BooleanType)
    .add("collapsed", DataTypes.BooleanType)
    .add("collapsed_reason", DataTypes.StringType)
    .add("controversiality", DataTypes.LongType)
    .add("created_utc", DataTypes.LongType)
    .add("distinguished", DataTypes.StringType)
    .add("edited", DataTypes.BooleanType)
    .add("gilded", DataTypes.LongType)
    .add("id", DataTypes.StringType)
    .add("is_submitter", DataTypes.BooleanType)
    .add("link_id", DataTypes.StringType)
    .add("no_follow", DataTypes.BooleanType)
    .add("parent_id", DataTypes.StringType)
    .add("permalink", DataTypes.StringType)
    .add("removal_reason", DataTypes.StringType)
    .add("retreived_on", DataTypes.LongType)
    .add("score", DataTypes.LongType)
    .add("send_replies", DataTypes.BooleanType)
    .add("stickied", DataTypes.BooleanType)
    .add("subreddit", DataTypes.StringType)
    .add("subreddit_id", DataTypes.StringType)
    .add("subreddit_name_prefixed", DataTypes.StringType)
    .add("subreddit_type", DataTypes.StringType)
}

