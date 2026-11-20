# nanoMuse 品牌规范 {#nanomuse-品牌}

本规范于 2026-09-24 确定。App 图标和界面配色采用同一套设计：界面的颜色取自图标，使 App 内外的视觉风格保持一致。

本页的设计变量（design token）是颜色等样式的统一名称，例如 `primary`。SVG 是可以无损缩放的矢量图格式，PNG 则是由像素组成的位图。

## 标志 {#the-mark}

App 标志采用 Hugeicons 的 **AI Brain 02**，使用免费的、未标注 Pro 的 *Stroke Rounded* 版本。我们检查了 AI 分类的全部 16 页；共有 143 个免费 rounded 选项，最终选择第 1 页的 AI Brain 02。保留了原图的三条路径、圆角端点与圆角连接。

- 源文件 `assets/brand/nanomuse-mark.svg` 保存 `@hugeicons/core-free-icons` 4.4.0 中 `AiBrain02Icon` 的原始 24 × 24 路径。该图标采用 MIT 许可证；归属说明和许可证全文见 `THIRD_PARTY_NOTICES.md`。
- `assets/brand/nanomuse-icon-source-1024.png` 是 1024 px 的导出图：品牌蓝背景上的白色圆角方块，不是矢量路径源文件。
- `assets/brand/nanomuse-icon.svg` 将白色圆角方块（`rx=27`）与标志组合。网页和桌面图标会加一圈 `#D9D9DE` 细边框，避免白底上看不清方块。
- `assets/brand/nanomuse-icon-on-blue.svg` 是带品牌蓝背景的版本，用于商店和启动场景；favicon、README 和一般 App 身份展示使用不带蓝色背景的白色方块。
- `assets/brand/nanomuse-mark-rgba-688.png` 是 688 px 的透明通道位图备用图。`docs/app-icon.png` 则是带透明外角和细边框的 512 px App 图标。
- `scripts/gen-brand-assets.py`、`scripts/gen-android-icons.py` 和 `scripts/gen-ios-icons.py` 会从同一套路径生成各平台资源。

App 图标与聊天形象用途不同。默认聊天形象是随附的小龙，资源位于 `web/public/avatars/` 和 Android App 的 `avatar/` 中。用户也可以选择带底色的 emoji，或在形象工作室生成自己的形象。早期使用的小熊猫已于 0.1.23 移除。导航和操作按钮的 UI 图标仍是独立的图标；小龙动画也仍属于聊天形象，不会被替换成 App 标志。

不要把小龙或旧版小熊猫用作启动器图标，也不要把 App 标志用作聊天形象。

## 颜色 {#colour}

以下颜色从图标中测得。

| 设计变量 | 值 | 用途 |
|---|---|---|
| `brand.stroke.start` | `#015CFB` | 标志渐变的起始颜色，位于左端 |
| `brand.stroke.end` | `#0186FB` | 标志渐变的结束颜色，位于右端 |
| `brand.blue` | `#0078FD` | 白色图标方块背后的纯色背景；启动/欢迎页的晕染背景使用标志渐变的浅色版本 |
| `tile` | `#FFFFFF` | 图标的白色方块 |

### 浅色主题 {#light-theme}

| 设计变量 | 值 | 对比度 | 用途 |
|---|---|---|---|
| `primary` | `#015CFB` | 白色背景上为 5.35 | 链接、带白色文字的主按钮、状态行 |
| `primary.container` | `#E5F0FF` | — | 选中行、标签 |
| `ink` | `#000000` | 白色背景上为 21 | 用户消息气泡配白字；发送和「回到最新」圆形按钮配白色箭头 |
| `pill` | `#F2F2F7` |  | 智能体的消息气泡 |
| `primary.tint` | `#EEF5FF` | — | 需要轻微突出显示的区域 |
| `bg` | `#FFFFFF` |  | 聊天背景、底部胶囊栏、菜单和抽屉面板 |
| `bg.grouped` | `#F2F2F7` | — | 设置页面，保留 OpenMinis 原有配色 |
| `surface` | `#FFFFFF` | — | 卡片和输入框 |

对比度表示前景与背景在亮度上的差异。数值越大，通常越容易分辨；这里的数值均对应表中指定的背景色。

### 深色主题 {#dark-theme}

| 设计变量 | 值 | 对比度 | 用途 |
|---|---|---|---|
| `primary` | `#58A6FF` | 在 `#000` 上为 8.3，在 `#1C1C1E` 上为 6.7 | 链接、带黑色文字的按钮、状态行 |
| `primary.container` | `#1A2B4A` | — | 选中行、标签 |
| `ink` | `#FFFFFF` | 在 `#000` 上为 21 | 用户消息气泡配黑字；发送和「回到最新」圆形按钮配黑色箭头 |
| `pill` | `#1C1C1E` |  | 智能体的消息气泡 |
| `bg` / `surface` / `surface.2` | `#000000` / `#1C1C1E` / `#2C2C2E` | — | 保留 OpenMinis 原有配色 |

界面只使用一种强调色。OpenMinis 原来分别用 iOS 蓝、橙、绿显示的代码块、思考文字和链接，统一改用 `primary` 和中性色。

对话区域以黑白灰为主：消息气泡、发送按钮和「回到最新」圆形按钮使用 `ink`；聊天背景保持中性或使用用户选择的背景。当前标签的胶囊是一个小例外，使用品牌渐变 `#015CFB` → `#0186FB` 和白色图标（渐变中最浅处对比度至少为 3.62:1）。欢迎、初次设置或加载界面可以使用非常浅且静态的蓝色渐变晕染；不要把它放在可读聊天记录的背后。其他控制图标保留原有形状和语义颜色。Android 的聊天颜色定义在 `ChatColors.kt` 中，由 `scripts/rebrand.py` 生成。小龙自身的颜色只用于形象，不作为界面配色。

## Android 中的对应实现 {#android-mapping-done-in-s1}

- 自适应图标由三层组成：背景层为纯白 `#FFFFFF`；前景层用 `VectorDrawable` 绘制 AI Brain 02 的路径，`strokeColor` 使用上述渐变，并采用圆角端点和圆角连接；单色层使用白色路径，由 Android 根据主题着色。
- 图标外观沿用 OpenMinis 的 activity 别名机制，即用不同启动入口显示不同图标。「自动」和「浅色」使用白色方块；「深色」使用 `#0F1B33` 方块和白色 AI Brain 02 标志。
- 通知栏小图标使用纯白标志，尺寸为 24 dp。dp 是 Android 按屏幕密度换算的界面尺寸单位。
- 发布时不得包含旧的 OpenMinis 图标、名称或字母 n 版图标草稿。

## 使用限制 {#don-ts}

- 标志只能使用蓝色渐变、纯白或纯黑。
- 不要旋转标志、添加描边或给笔画加阴影。
- 标志放在品牌蓝背景上时，必须保留白色方块，以保证对比度。
- 不要使用其他产品的标志、名称或品牌蓝作为素材，只使用 nanoMuse 自己的标志。
