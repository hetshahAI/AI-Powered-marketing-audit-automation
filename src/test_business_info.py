from collectors.business_info import extract_business_info

url = "https://www.americanhorizonproperty.com/"
info = extract_business_info(url)

for key, value in info.items():
    print(f"{key}: {value}")
