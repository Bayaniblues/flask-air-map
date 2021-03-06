import openaq


def testing():
    api = openaq.OpenAQ()
    status, body = api.cities()
    print(status)
    print(body)


def los_angeles():
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    print(status)
    print(body)


if __name__ == '__main__':
    los_angeles()
