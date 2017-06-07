# Discord Bot
Another python bot for Discord chat
# Installation
Basically, all you need to do to install is make a `config.json` file like the following:

```json
{
    "botkey": "Discord app bot user token",
    "github": {
        "username": "github name",
        "pass": "password"
    }
}
```

# Commands

### Help
*Description*: Displays all of the commands available.

*Usage*: `!!help`

### Hello
*Description*: Say hi to the bot (says hello world back)

*Usage*: `!!hello`

### XKCD
*Description*: Shares a XKCD comic, with an optional number

*Usage*: `!!xkcd <comic-number>` or `!!x <comic-number>` or `!!x`

### Iconify
*Description*: Turns a string into a list of emoji

*Usage*: `!!iconify <string>` or `!!i <string>`

### Cat
*Description*: Shares a random cat photo from [random.cat](http://random.cat)

*Usage*: `!!cat` or `!!c`

### Dog
*Description*: Retrieves and shares a random dog photo from [random.dog](http://random.dog)

*Usage*: `!!dog` or `!!d`

### Shib
*Description*: Shares a random photo of Shiba Inu, using RobIsAnxious's database [here](https://github.com/RobIsAnxious/shibesbot-db) 

*Usage*: `!!shib` or `!!s`
