import random

@bot.command(name="roll save ", help="rolls for a character's saving throw with the given 3-letter stat")
async def roll_save(ctx, save_input):
    # pulls the correct stat from the character sheet
    save_attribute = "attr" + save_input.capitalize
    save_stat = int(data[member.name][0][save_attribute])

    # turns the stat into a +- modifier
    save_int = (save_stat//2) - 5

    # check for saving proficiency, adds to modifier
    if save_input.capitalize in data[member.name][0][savingThrows]:
        save_int += int(data[member.name][0][profBonus])

    #rolls the dice, adds the modifier, and sends back the result
    dice = random.randint(1,20) + save_int
    await ctx.send(dice)