---
title: Adventures with Kafka
slug: kafka-adventures
date: 2018-10-24 16:14:00 UTC
---

# Kafka Streaming Evaluation

### Part 1: Near Real-Time Environment Monitoring

We started looking at the Kafka Streaming Platform as we explored options for monitoring our upcoming enterprise management applications. The consulting company that was implementing the enterprise solution was not providing any monitoring capabilies (and in fact did not implement logging in any consistent way). It fell to us, me in particular, to explore possible ways to be able to monitor the environment. After some initial exploration of how other enterprises were solving these kinds of problems, we decided to evaluate streaming as provided by Kafka for a proof-of-concept monitoring application. Our server teams gave me 3 VMs and sudo, and I installed and configured the various components of the Kafka platform.

The specific problem that we wanted to address was that QA and business people were testing various components of the enterprise environment but encountering performance issues. Testers could not easily determine whether they were seeing a problem with the implementation of their use case, a problem with the server they were connecting to, or a problem with a connected component elsewhere in the environment. Almost all of the systems were hosted on components of the Oracle enterprise stack, and the systems were being monitored by Oracle Enterprise Manager (OEM), but OEM is not a tool for users. However, OEM can be configured to send SNMP traps to an address, and we decided to leverage SNMP to provide simple but timely component status to the tester community.

The first challenge was to get data from the SNMP traps into a Kafka stream. I had to learn a bit about SNMP, its versions, and how to interpret the data. I needed to develop a microservice that would listen to incoming SNMP traps, extract the relevant data, and publish events to a stream. A Java SNMP connector on Github looked promising, but it required SNMP V2 and OEM only supported V1 and V3. I found a Python library, PySNMP, that allowed me to listen for SNMP traps from OEM and also grab some data from them to publish to my snmp-traps stream as JSON.

Next, I wrote a simple Python service to consume what was essentially raw SNMP trap data and extract the handful of values that I cared about, and publish to an alert stream, again as JSON.

The final piece was the most challenging: presenting an up to the minute summary of environment status in a web page. I was dealing with 11 tiers, 4 main server types, and over 50 individual servers for which to display the latest status and trend. The display needed to be updated in realtime with no user interaction, primarily for display on a kiosk monitor. I knew I wanted to use the WebSocket protocol, but I didn't know how. I couldn't use Server-sent Events (SSE) because I also needed to support IE on user desktops.

I found a very interesting Python networking platform designed for distributed messaging applications, Crossbar.io. Crossbar supports the WebSocket protocol, includes asynchronous servers, and has numerous sample applications including a demo network event monitoring daemon written in Python for the server side and React on the client side. While the example app was the authors' first Crossbar.io app and their first React.js app (and mine, as well), it nevertheless provided enough scaffolding that I could adapt for my needs. I implemented a Kafka consumer component in the server app that would listen for alert events from the alert stream. My primary need could most quickly be met by maintaining state and generating the core UI on the server side, so I used React in only the most rudimentary way. The application built and persisted a matrix of server status and history, and each time an alert event arrived, the matrix was updated. In addition, an HTML grid component was updated and pushed through the WebSocket connection to each connected browser client, where React handled the page updates.

The overall application performed well and was very robust. It had at least two main issues: history persisted and reported on servers that had been retired (deleting the persisted data structure was the manual workaround); and connecting a new browser client did not trigger a full refresh of the status grid, only an new SNMP event accomplished this.

### Part 2: ETL

Subsequent to our monitoring POC, my company shifted direction and walked away from the never-completed enterprise application stack that a rather well-known consulting company had been developing for us. At that point, we realized that implementing "Plan B" required us to implement an application integration platform. Kafka seemed like a good candidate solution (along with others) and we started a second phase of evaluation. For this work, our server team built and configured a small cluster of Kafka platform servers using Chef. Our first target was testing some data conversion and integration activities that required some data transformations.

It seemed to me that what we were trying to do matched some of the use cases for the emerging (at the time, it was in beta) KSQL component of the Kafka platform. I was able to configure a Kafka Connect instance to read data from a database and publish it to a stream in Avro format. This provided a basis for experimenting with some of the functions supported by KSQL. However, I was unable to get more than one transformation function working at a time when creating a new, transformed stream from an existing stream. I then tried using the Kafka Streams Java library and attempted to do some stream joins. This seemed to work but sometimes I ended up with duplicate data in the output streams. Later I discovered that the method I was using to truncate my input streams between tests did not actually purge the data and it was duplicate input that resulted in duplicates in the output.

After a couple of disappointing experiments, I reverted to the tried-and-true approach of creating Python programs to perform transformations from one stream into another. This worked just fine, was easy to implement and fast to execute, but was not an approach that could easily be adopted by our business analysts (in the case of KSQL) or our Java developers (in the case of Kafka Streams).

### Part 3: Speed Test

As the final part of our integration platform evaluation, we wanted to compare performance when running data integration or conversion processing. We're not talking huge volumes here, the worst case conversion scenario is less than 60 million records. For our speed test comparison, we essentially copied 1.7 rows from a DB2 table on our AS/400 into a table in Oracle. No transformations were performed, but column names were slightly different in DB2 (due to limits on the length of a column name). We compared Kafka, Oracle Data Integrator (ODI), MuleSoft, and Microsoft's SSIS tool. I configured Kafka Connect source and sink JDBC connectors and deployed one of each to servers (not part of our Kafka cluster). Each product test was run separately so that there would not be contention.

As I expected, Kafka was the fastest, tranfering the data in 6 minutes. ODI and Mule each clocked in at about 7 minutes, and SSIS came in at 10 minutes. In a subsequent run, I deployed 3 Connect sink workers, each on a separate server, and after I started the Connect source worker, the transfer completed in about 4 minutes.

### Conclusion

Despite the performance, versatility, scalability, and price (we were using the OSS Confluent package) advantages of Kafka, management decided that MuleSoft was the best solution for our organization.

However, I had a lot of fun learning about and experimenting with Kafka, and I'm sorry we will not be using it in the future. I think it is an excellent and exciting way of implementing systems.
