# merge generated data
import src.data_generate_yehoon as yh

data = []

data.extend(yh.gen_data())

print(len(data))
print(data[:5])
print(data[-3:])


