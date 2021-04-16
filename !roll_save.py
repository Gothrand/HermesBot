import random

@bot.command(name="roll save ", help="rolls for a character's saving throw with the given 3-letter stat")
async def roll_save(ctx, save_attribute):
    # pulls the correct stat from the character sheet
    save_attribute = "attr" + save_attribute.capitalize
    save_stat = int(data[member.name][0][save_attribute])

    # turns the stat into a +- modifier
    save_int = (save_stat//2) - 5

    #rolls the dice and sends back the result
    dice = random.randint(1,20) + save_int
    await ctx.send(dice)