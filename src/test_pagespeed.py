from collectors.pagespeed import get_website_performance

url = "https://www.americanhorizonproperty.com/"
perf = get_website_performance(url)

for key, value in perf.items():
    print(f"{key}: {value}")
