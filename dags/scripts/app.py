from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
# from pyspark.sql.connect.functions import concat
# import pandas
import os
import sys

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
# import pyarrow
# Create SparkSession
spark = SparkSession.builder \
      .appName("SparkByExamples.com") \
      .getOrCreate()
'''
df = spark.read.format('csv').option("header","true").option("inferSchema","true").load("D:/Apache_Spark\csv\customers-1000.csv")
df.printSchema()
# df.show()
# df = spark.createDataFrame([(1,'Adithya'),(2,"Sravani"),(3,"Chitti")],("id","name"))
df.groupby('Country').agg(count('*').alias('Count')).show()
'''


customer_data = [(1,'manish','patna',"30-05-2022"),
(2,'vikash','kolkata',"12-03-2023"),
(3,'nikita','delhi',"25-06-2023"),
(4,'rahul','ranchi',"24-03-2023"),
(5,'mahesh','jaipur',"22-03-2023"),
(6,'prantosh','kolkata',"18-10-2022"),
(7,'raman','patna',"30-12-2022"),
(8,'prakash','ranchi',"24-02-2023"),
(9,'ragini','kolkata',"03-03-2023"),
(10,'raushan','jaipur',"05-02-2023")]

customer_schema=['customer_id','customer_name','address','date_of_joining']


sales_data = [(1,22,10,"01-06-2022"),
(1,27,5,"03-02-2023"),
(2,5,3,"01-06-2023"),
(5,22,1,"22-03-2023"),
(7,22,4,"03-02-2023"),
(9,5,6,"03-03-2023"),
(2,1,12,"15-06-2023"),
(1,56,2,"25-06-2023"),
(5,12,5,"15-04-2023"),
(11,12,76,"12-03-2023")]

sales_schema=['customer_id','product_id','quantity','date_of_purchase']


product_data = [(1, 'fanta',20),
(2, 'dew',22),
(5, 'sprite',40),
(7, 'redbull',100),
(12,'mazza',45),
(22,'coke',27),
(25,'limca',21),
(27,'pepsi',14),
(56,'sting',10)]

product_schema=['id','name','price']


customer_df = spark.createDataFrame(data=customer_data,schema = customer_schema)
sales_df = spark.createDataFrame(data=sales_data,schema =sales_schema)
# product_df=spark.createDataFrame(data=product_data,schema =product_schema)

# customer_df.show()
# sales_df.show()
sales_df = sales_df.repartition(3)
customer_df = customer_df.repartition(3)
# print(customer_df.rdd.getNumPartitions())
# print(sales_df.rdd.getNumPartitions())
print(customer_df.printSchema())
print(sales_df.printSchema())
joined_df = customer_df.join(sales_df,sales_df['customer_id']==customer_df['customer_id'],'inner').drop(sales_df['customer_id'])
print(joined_df.collect())
# joined_df.coalesce(1).write.mode('overwrite').format('csv').option('header','true').save('file:///D:/AirflowInLenovo/Airflow_practice')
joined_df.coalesce(1).write.mode('overwrite').format('json').option('header','true').save('/opt/airflow/dags/scripts1/')
