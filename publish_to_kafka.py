#Add this where you want to publish your message

# payload = {
#   "Name": VedantVartak,
#   "Age": 25,
#   "Gender": "Male"
# }

try:
    publish_to_kafka(payload)
except Exception as e:
    logger.error("Kafka error while publishing payload : ", e)
