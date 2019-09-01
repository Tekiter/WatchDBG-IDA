# WatchDBG-IDA
비주얼 스튜디오에서 볼 수 있던 조사식 창을 IDA 디스어셈블러에서 사용해 보세요!

## 설치
IDA 설치폴더의 `plugins` 폴더(기본값: `C:\Program Files\IDA 7.0\plugins`)에 `WatchDbg`폴더와 `WatchDbg.py`파일을 복사해 넣으세요.

## 사용법

#### 동적 디버그 사용 중

- `Shift + A` 키로 새 조사식을 등록합니다.
- `Shift + W` 키로 조사싱 창을 엽니다.

등록된 조사식은 디버깅 진행시 자동으로 실시간 업데이트 됩니다.

#### 조사식 등록
- 메모리 주소를 직접 입력할 수 있습니다. (`0x4003a8`, `602194`)
- 주소 연산 식도 가능합니다. (`0x4007b0 + 0x10 * 4`)
- 레지스터도 사용할 수 있습니다. (`rsp`, `rbp-0x48`)

#### 조사식 창
- `X` 버튼으로 모든 조사식을 지웁니다.
- `+` 버튼 또는 A키로 새 조사식을 등록합니다.
- `T` 버튼 또는 T키로 조사식 타입을 변경합니다.
- `N` 키를 눌러 조사식의 이름을 변경합니다.

## 사용 가능 타입
- `int8, int16, int32, int64, ...` (부호 있는 정수형)
- `uint8, uint16, uint32, uint64, ...` (부호 없는 정수형)
- `float, double`
- `ptr or pointer`
- `char, str or string`


배열은 `[type] [size]` 와 같이 입력하여 사용할 수 있습니다. 이 경우 `type arr[size];` 와 같은 의미가 됩니다.

예를 들어, `int32 5` 은 C에서의 `int32 arr[5];` 와 같은 타입입니다.
또한, `char 3 4 5` 은 C에서의 `int8 arr[5][4][3];` 와 같은 타입입니다.


## Screenshots
![Overview](https://github.com/Tekiter/WatchDBG-IDA/blob/master/media/screenshots/overview.PNG "Overview Screenshot")
![Overview](https://github.com/Tekiter/WatchDBG-IDA/blob/master/media/screenshots/overview2.PNG "Overview Screenshot")
![Overview](https://github.com/Tekiter/WatchDBG-IDA/blob/master/media/screenshots/arr1.PNG "Overview Screenshot")
![Overview](https://github.com/Tekiter/WatchDBG-IDA/blob/master/media/screenshots/arr2.PNG "Overview Screenshot")
![Overview](https://github.com/Tekiter/WatchDBG-IDA/blob/master/media/screenshots/ptr.PNG "Overview Screenshot")
