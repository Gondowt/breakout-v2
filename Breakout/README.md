# breakout-project
Python project

Pour lancer le container docker (commande réalisé sous ubuntu):

1. Vérifier que les connexions externes sur l'environnement graphique sont autorisé,
si elles le sont pas :
xhost +
2. Ensuite on build l'image docker à partir du Dockerfile :
sudo docker build -t breakout .
3. Enfin on run l'image comme un container :
sudo docker run -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix breakout
