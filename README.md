# WatchDBG-IDA
Add a watch view to your IDA 7.0 similar to Visual Studio's watch view!

[Download](https://github.com/Tekiter/WatchDBG-IDA/releases)

## Install
Put everything in `src` directory to `plugins` directory of your IDA installation.

## Usage

#### While you are debugging...

- `Shift + A` to add a watch.
- `Shift + W` to show watch view.

And just continue debugging. Changed values in watch will be automatically updated.

#### Add Dialog
- You can type memory address (`0x4003a8`, `602194`)
- Expressions are also allowed (`0x4007b0 + 0x10 * 4`)
- Or use register's value (`rsp`, `rbp-0x48`)

#### Watch View Window
- Click `X` button to remove all watches.
- Click `+` button or press `A` key to add a new watch.
- Click `T` button or press `T` key to change watch type.
- Press `N` key to change watch's name

## Available types
- `int8, int16, int32, int64, ...` for integer values
- `uint8, uint16, uint32, uint64, ...` for unsigned integer values
- `float, double`
- `ptr or pointer`
- `char, str or string`

`[type] [size]` will be converted to `type arr[size];`

For example, `int32 5` will be converted to `int32 arr[5];`

Furthermore, `char 3 4 5` will be converted to `int8 arr[5][4][3];`



## Screenshots
![Overview](https://github.com/Tekiter/WatchDBG-IDA/blob/master/media/screenshots/overview.PNG "Overview Screenshot")
![Overview](https://github.com/Tekiter/WatchDBG-IDA/blob/master/media/screenshots/overview2.PNG "Overview Screenshot")
![Overview](https://github.com/Tekiter/WatchDBG-IDA/blob/master/media/screenshots/arr1.PNG "Overview Screenshot")
![Overview](https://github.com/Tekiter/WatchDBG-IDA/blob/master/media/screenshots/arr2.PNG "Overview Screenshot")
![Overview](https://github.com/Tekiter/WatchDBG-IDA/blob/master/media/screenshots/ptr.PNG "Overview Screenshot")
