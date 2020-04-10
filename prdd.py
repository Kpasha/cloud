# -*- coding: utf-8 -*-
"""PySpark_RDD.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OdUZdkW5tv12a0fNvTaDGfo16AAOu7qh

## Install JDK
## Install Spark
## Set Environment variables
## Create a Spark Session
"""

!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q http://apachemirror.wuchna.com/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz
!tar -xvf spark-2.4.3-bin-hadoop2.7.tgz
!pip install -q findspark
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-2.4.3-bin-hadoop2.7"
import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()

"""## Test Spark"""

df = spark.createDataFrame([{"Google": "Colab","Spark": "Scala"} ,{"Google": "Dataproc","Spark":"Python"}])
df.show()

"""## Copy a data file to your local Colab environment"""

!wget https://raw.githubusercontent.com/futurexskill/bidata/master/retailstore.csv

"""## Check if the file is copied"""

!ls

"""# Resilient Distributed Dataset (RDD)

## Import SparkContext and SparkConf
"""

from pyspark import SparkContext

"""## Create Spark Context from Spark Session"""

sc = spark.sparkContext

"""## Create a RDD from Python List"""

sampleRDD = sc.parallelize([10,20,30,40,50,60])

type(sampleRDD)

sampleRDD.collect()

"""## Read the CSV file into a RDD"""

customerData = sc.textFile("retailstore.csv")

type(customerData)

"""## Perform RDD Operations

Print all records
"""

customerData.collect()

"""Print count"""

customerData.count()

"""Print the fist row"""

customerData.first()

"""Fetch the first 3 rows"""

customerData.take(3)

"""Print each row"""

for line in customerData.collect():
    print(line)

"""### Map

Replace "Male" with "M"
"""

customerData2 = customerData.map(lambda x : x.replace("Male","M"))

customerData2.collect()

"""### Filter

Display only females
"""

femaleCustomers=customerData.filter(lambda x: "Female" in x)

femaleCustomers.collect()

femaleCustomers.count()

"""### flatMap

Create a new RDD by splitting each row with comma delimeter
"""

words=femaleCustomers.flatMap(lambda line: line.split(","))

words.count()

words.collect()

"""### Set - Union & Intersection"""

rdd1 = sc.parallelize(["a","b","c","d","e"])
rdd2 = sc.parallelize(["c","e","k","l"])

"""Perform Union operation"""

for unions in rdd1.union(rdd2).distinct().collect():
    print(unions)

"""Perform Intersection operation"""

for intersects in rdd1.intersection(rdd2).collect():
    print(intersects)

"""### Transformation using function"""

customerData.collect()

"""Define the transformation method"""

def transformRDD(customer) :
    words =customer.split(",")
    #convert male to 0 and female to 1
    if words[2] == "Male" :
         words[2]="0"
    else :
         words[2]="1"
    #Convert N to 0 and Y to 1 for the purchased value
    if words[4] == "N" :
         words[4]="0"
    else :
         words[4]="1"
    #Convert Country to upper case        
    words[3] = words[3].upper()
    return ",".join(words)

"""Apply transformation using map"""

transformedCustData=customerData.map(transformRDD)

transformedCustData.collect()

"""## reduce"""

sampleRDD = sc.parallelize([10, 20, 30,40])

sampleRDD.reduce(lambda a, b: a + b)

