# Console Alarm
**Console alarm** is a small alarm function for your console.

## Important
* For now just tested on ubuntu.

## Dependencies
* [PyGame](https://www.pygame.org/) and [NumPy](https://numpy.org) for creating the alarm sound.

## Usage
**Console alarm** is usable with one or two numeric arguments

### One argument:
If there is only one argument it is interpreted as minutes. The alarm will act
as a pomodoro that rings after the set minutes.

e.g. `./alarm 5`

### Two arguments:
With two arguments, you will set an alarm clock for a specified time.
If you set 14 09 as arguments, the alarm will start at 14:09.

e.g. `./alarm 14 09`

## Documentation
For more information take a look at the documentation at
[www.ruerob.com](http://www.ruerob.com/console_alarm/console_alarm.html).

## Nice to know
On Ubuntu you can put this task into background with 'ctrl+z' and then run 'bg'
Get it to the foreground again with fg