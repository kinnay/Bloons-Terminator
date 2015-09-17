# Bloons-Terminator
A custom Bloons TD Battles client

This client connects to the ninjakiwi servers. As you can see when you browse through the source code, they invented a funny protocol. Messages are just plain text, with commands like "GimmeUrPlayerInfo". This client starts a quick battle by default, but you can also make it find a custom battle by editing the source code in the MenuClient class.

While in the preparation stage, you can see which towers the opponent picks. When the opponent spends battle energy to snoop your towers, he'll see... 4 monkey buccaneers :P

When the game has started, this client sends a message through the chat, telling the opponent what to do. He's supposed to send commands to the bloons terminator. Some people seem to not understand what they should do, and surrender, even though they could easily receive a win by sending the /surrender or /disconnect command through the chat. Other people are more intelligent and start sending commands to the terminator. It's always fun to see how surprised and amazed those people are. Sometimes they say that they're going to report you to the ninjakiwi staff, but since this client doesn't even need an account to connect to the servers, they can't ban.

The game usually ends when the opponent dies or makes the bloons terminator /disconnect or /surrender. Sometimes they send a ZOMG at themselves early and die quickly. Sometimes the opponent plays more than 30 rounds though.

Here are a few examples of the output of this client:
http://pastie.org/10426304
http://pastie.org/10426307
http://pastie.org/10426369