from predictor import predict_customer


customer = {

    "Age":35,
    "Country":"USA",
    "Gender":"Male",

    "Customer_Support_Contacts":3,
    "Days_Since_Last_Purchase":20,
    "Purchase_Count":5,
    "Total_Spent":500,

    "Resolution_Time_Hours":10,

    "Review_Text":
    "The product is great but customer support is not helpful"
}


result = predict_customer(customer)

print(result)