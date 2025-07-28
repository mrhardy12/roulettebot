# Roulette assistance bot.

## Overview:
Plays roulette for tabletop RPGs such as Dungeons and Dragons. Accepts any number of players and bets. Recommended usage: 6 or fewer players, 8 bets per player maximum. There is no inherent maximum, but for game scale it makes it much easier. The program uses arbitrary valueless "chips" to represent player resources; this can be substituted for dollars or gold/silver/copper coins or any other currency you desire, though the program does not contain a way to handle that conversion for you. You will have to manually treat any print of "chips" as "$" in your mind.

The game *does not* have inherent handling for negative chip counts; simply do not allow players to bet in a way that would leave them negative as the game master. This is a helper bot to do the hard work of tracking players' chips for you, not a bot that runs the entire game by itself. The game is meant to be used by a game master running an active roleplaying game with their friends.

## Basic commands:
Bot will loop until ended. First, it will ask how many players will be starting at the table. Enter that number and it will ask you to input their names. Next, it asks how many bets each player placed on the first round of betting. Gather the bets from some other source, such as the table or Discord. The limitations on betting speed are up to the user. The bot will then ask for each player's bets, in order of player name inputs. The inputs for bets are as follows.

## Bet logic:
### Integer (straight-up):
For single number bets between 1 and 36, simply type the number between 1 and 36 (inclusively) and press Enter.

### Edge (split):
For bets on two numbers at once (such as a bet on the border between 4 and 7), enter either "*H*orizontal *E*dge" or "*V*ertical *E*dge" shortened to an acronym as a prefix ("HE" and "VE", respectively), along with the first number of the bet. A bet on 4 and 7 would be input as "VE4" into the terminal. A bet on 4 and 5 would be entered as "HE4" instead. Both of these implement error handling; horizontal bets on a number divisible by 3 subtract 1 from the input number (HE3 would be treated as HE2), and vertical bets subtract 3 from the input on 34, 35, or 36 (VE34 would be treated as VE31).

### Zero bets:
For bets on 0 or 00, enter "ZE0" or "DZ00" respectively. For bets on *both* zeroes, instead enter "ZZ" to represent "both zeroes".

### Row (street):
For bets on rows, simply enter "RO" as a prefix with a number. Example: RO4 and RO5 would both produce the same result: the row that contains 4, 5, and 6.

### Double-Row (Six-Numbers):
For bets on two rows at once, such as a bet on the row 4-5-6 and 7-8-9 in a single bet, enter "DR" as a prefix and a number in the first row being bet on. An input of DR6 would produce the result in this example: a bet on 4-5-6-7-8-9. There is inherent error handling here: if you enter DR35, for example, there is no row that begins with 37. Therefore, it just subtracts 3 and treats the input as if you had typed "DR32" instead.

### Corner:
For bets on corners between four numbers, enter "CR" as a prefix and the number of the *upper-left* value. An input of CR1 will be a bet on 1-2-4-5, while an input of CR2 will be a bet on 2-3-5-6. To prevent indexing errors, this also subtracts from input on any "outer" row or column. CR3 would be treated as CR2, and CR34 as CR31. CR36 implements both of these hotfixes, being treated as CR32.

### Column:
For bets on a column, enter "CO" as a prefix and then a number that appears in the column. Any number is valid between 1 and 36; it just takes the number modulo 3 (and adds 3 if 3 mod 3 = 0), and treats that as the input instead. CO14 should produce the same result as CO2. I do recommend just using CO1, CO2, or CO3 even still, though, just to make it easier on yourself.

### Bets without prefixes:
All other "regional" bets such as a dozens bet or a lows bet simply use two-letter inputs. These inputs are:
    HD - High Dozen (25 through 36 inclusive)
    MD - Middle Dozen (13 through 24 inclusive)
    LD - Low Dozen (1 through 12 inclusive)
    RE - Reds (based on real American roulette table colorations)
    BL - Blacks (based on real American roulette table colorations)
    LO - Lows (1 through 18 inclusive)
    HI - Highs (19 through 36 inclusive)
    OD - Odds
    EV - Evens
    FN - Five Numbers. This is specifically used for a "double row" bet on *exactly* 0, 00, 1, 2, and 3, and is something that casinos allow.
    ZZ - Both Zeroes. This is a bet on exactly 0 and 00, and is handled like a split bet by game logic.

### Invalid inputs:
Any bet input that does *not* meet one of these patterns will result in the bet being skipped and a message being printed that explains the same commands as this README file, as do bets outside the range of 1-36 entered as a number. A bet on 0 *must* be input as ZE0 instead.

## Spinning:
After bets are placed, press "Enter" to spin the wheel, then press "Enter" again to have the program calculate payouts. Payouts are based on real-world ratios, determined by the formula (36/n) - 1 where n is the number of "winning" numbers bet on by that single bet. A bet on reds, which has 18 winning numbers, pays out at (36/18) - 1 = 1x. A bet on a split pays out at (36/2) - 1 = 17x. The program handles all of this for you for every bet, and outputs the player's new chip count.

Technically speaking, any input that is not an interrupt (discussed in next section) will work here, as you are pressing "Enter" to input the text. However, no inputs here will be captured. The only thing that matters is that you pressed "Enter".

## Input interrupts:
You may have players who wish to join or leave the table partially into the game. The code allows for this via "interrupts": at any time, an input of "add" will add a player, and an input of "remove" will remove a player. The new player changes will not apply until the round of betting is over, so make sure to input a removed player's bet count as 0.

Another interrupt is "end", which exits the program immediately. This is primarily for emergency use, such as suddenly needing to leave the computer. I do not recommend using the "end" interrupt unless absolutely necessary, as you will not get a final scores output by doing so.

The final interrupt is "status", which displays current players and their remaining chips. Note that this will *not* display an accurate chip count while inputting bets, as chips have not been added or deducted at this time.

Players who leave the game and return will have their chip counts retained, allowing them to enter the game again.

## Round advancement:
After the spin is complete and the new chip totals are tallied and printed for each player, the program will ask if you would like to continue playing. If you input "N" or "n", it will exit the program and print the final standings. Any other input that is not an interrupt will simply not be captured and the next round will begin as normal. The game loops back to the beginning of the Bet logic section, and play continues until the game master (you, as the user) decides to stop.