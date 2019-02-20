package trenddit

import org.apache.spark.ml.PipelineModel
import org.apache.spark.sql.DataFrame

object RandomForestModel{
    private val model_path = "models/..."

    private val model = PipelineModel.read.load(model_path)

    def transform(df: DataFrame ) = {
        val df_clean = df.na.fill(0)

        val result = model.transform(df_clean)

        result.show()
    }
}
