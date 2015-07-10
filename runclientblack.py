import client, indochineplayer

#replace randomplayer.RandomPlayer with your player
#make sure to specify the color of the player to be 'B'
blackPlayer = indochineplayer.IndoChinePlayer('B')

blackClient = client.Client(blackPlayer)
blackClient.run()
