from wit import Wit

client = Wit("L2SE6YQB54PDESGSR5S5HPCTXFEVB4A7")
resp = client.message('Give me some information on Amy Acker')
print(resp['intents'][0]['name'])

