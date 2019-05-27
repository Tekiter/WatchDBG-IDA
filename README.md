# WatchDBG-IDA
Add a watch view to your IDA similar to Visual Studio's watch view!

## Install
Put everything in `src` directory to `plugins` directory of your IDA installation.

## Usage

#### While you are debugging...

- Shift + A to add a watch.
- Shift + W to show watch view.

And just continue debugging. Changed value will automatically show up.

#### Watch View Window
- Click `X` button to remove all watches.
- Click `+` button or press `A` key to add a new watch.
- Click `T` button or press `T` key to change watch type.

## Available types
- `int8, int16, int32, int64, ...` for integer values
- `uint8, uint16, uint32, uint64, ...` for unsigned integer values
- `ptr or pointer`
- `char, str or string`

`[type] [size]` will be converted to `type arr[size];`

For example, `int32 5` will be converted to `int32 arr[5];`

Furthermore, `char 3 4 5` will be converted to `int8 arr[5][4][3];`



## Screenshots
![Overview](https://github.com/Tekiter/WatchDBG-IDA/blob/master/media/screenshots/overview.PNG "Overview Screenshot")
