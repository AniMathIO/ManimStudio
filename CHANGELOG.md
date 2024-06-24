# Changelog

## 1.0.0 (2024-06-24)


### ⚠ BREAKING CHANGES

* **ci/cd:** working on ci/cd system dependency fix
* **ci/cd:** working on docs generation fix
* **ci/cd:** working on ci/cd fix
* **ci/cd:** fix docmentation building action
* **app:** fixed faulty image stretching while resizing window
* **app:** fixed UI errors for resizing the windows without its contents correctly
* **app:** removing unnecessary event that caused exception

### Features

* **app:** enabled type checking via ruff ([a0a138a](https://github.com/AniMathIO/ManimStudio/commit/a0a138ad764010c5602fa196c297cd9c62ad218e))
* **app:** fixed faulty image stretching while resizing window ([b6285bb](https://github.com/AniMathIO/ManimStudio/commit/b6285bb55552e3413466f1f0240e30bda1f22fba))
* **app:** implemented base design ([0890a99](https://github.com/AniMathIO/ManimStudio/commit/0890a9964ca8735363e8d1c12084a5abb485573f))
* **app:** implemented project creation and project loading ([1655fb9](https://github.com/AniMathIO/ManimStudio/commit/1655fb9f9ad82ad0b01295ce50df5b68c9ab06aa))
* **app:** implemented proper logging ([c7aa7b5](https://github.com/AniMathIO/ManimStudio/commit/c7aa7b5f0ad473f87230e9e1224dd95d468881b0))
* **app:** implemented starting welcomepage and moved settings to the menubar ([c3d8cbf](https://github.com/AniMathIO/ManimStudio/commit/c3d8cbfc52886ac6f532f5ff6ca164a4187c3bd3))
* **app:** implemented user level configuration, and project creation ui and logic ([9dd5684](https://github.com/AniMathIO/ManimStudio/commit/9dd5684efc956191b98d1932c3202c2cf7806c11))
* **app:** installed dill ([58f0dea](https://github.com/AniMathIO/ManimStudio/commit/58f0deade394581d4fbac877dd6f15f4c4a59e23))
* **app:** installed rich for richtext logs ([a52f3cd](https://github.com/AniMathIO/ManimStudio/commit/a52f3cda208010502c06a0f226b29dd62b814514))
* **app:** installed structlog ([ad26220](https://github.com/AniMathIO/ManimStudio/commit/ad262206da2efda3a2000140f6c440258bb42dd5))
* **app:** refactored casing ([9291425](https://github.com/AniMathIO/ManimStudio/commit/92914257073148793f90873486c7c1dd408e19c6))
* **app:** reformatted code with ruff and added type hints ([31810d8](https://github.com/AniMathIO/ManimStudio/commit/31810d878c3bb87487f6a30b3f2f69987fb3d9f7))
* **app:** working on recent project list view ([f37c326](https://github.com/AniMathIO/ManimStudio/commit/f37c3267a350b25991564e596d9e8c138af3c759))
* **ci/cd:** created github action workflow for generating releases ([1c4c579](https://github.com/AniMathIO/ManimStudio/commit/1c4c579e2bf260e5a92780df1267f9c578f8c514))
* **ci/cd:** working on docs generation fix ([23f24fd](https://github.com/AniMathIO/ManimStudio/commit/23f24fdecaef26270eb8a98a8195925f012f580d))
* **docs:** added logos to readme and documentation ([6f20262](https://github.com/AniMathIO/ManimStudio/commit/6f20262b615a7d9c8a525e39fe623c8ed2f325b1))
* **docs:** added workflow badges to readme ([dcc7a74](https://github.com/AniMathIO/ManimStudio/commit/dcc7a7489e60c57d321c4dadfce4ac5c4aa1c1b8))
* **docs:** implemented action ([206e55e](https://github.com/AniMathIO/ManimStudio/commit/206e55ec04c057dca58ce4403f01aa4cd148be82))
* **docs:** implemented contribution guidelines ([913e7a6](https://github.com/AniMathIO/ManimStudio/commit/913e7a60511bb90016b8c28b29b36296115d2851))
* **docs:** implemented initial doc configurations ([971b7a1](https://github.com/AniMathIO/ManimStudio/commit/971b7a1ea4c03f9e7e44af1bcd308496885bbabf))
* **docs:** updated docs with the additional videoeditor module ([a28d379](https://github.com/AniMathIO/ManimStudio/commit/a28d3794d7aac1e90e8cfc70444f4244dccc9698))
* **docs:** updated documentation for theming feature ([94dca36](https://github.com/AniMathIO/ManimStudio/commit/94dca364b36570ceaaf4c6074f04f980d715bdc5))
* **docs:** updated documentation generation with the project opening and creating modules ([48f75eb](https://github.com/AniMathIO/ManimStudio/commit/48f75eb27a4a2b644591d54186718f2b6685789d))
* **docs:** updated documentation with utils module and logger utility ([500f128](https://github.com/AniMathIO/ManimStudio/commit/500f1281229e9bdd7a810bb78a9feba5a943276f))
* **logger:** implemented base logger utility ([a8f7f09](https://github.com/AniMathIO/ManimStudio/commit/a8f7f09849922873f75479d61adf3ce935d438bc))
* **logger:** implemented cleanup function for older logs, added type hints and reformatted code with ruff ([88775dc](https://github.com/AniMathIO/ManimStudio/commit/88775dc55fa42384762c12e51ade4fc401d787ae))
* **logger:** updated the logger utility to be more colorful ([a9951e7](https://github.com/AniMathIO/ManimStudio/commit/a9951e784eaabe61d9755a4c7369b84ed0006f84))
* **main:** added python docstrings to base project ([1e37820](https://github.com/AniMathIO/ManimStudio/commit/1e37820f958751df17fd8f181b5aeed361a2bcbb))
* notification about rebranding ([f43068f](https://github.com/AniMathIO/ManimStudio/commit/f43068f3dc1b8e56a8fcfead798cfea486105006))
* **project:** initial commit ([7ae1e1c](https://github.com/AniMathIO/ManimStudio/commit/7ae1e1c5349a96d2cb57642a9ea5ae4a6e2f2021))
* **settinfs:** added error handling for file operations ([c5dae28](https://github.com/AniMathIO/ManimStudio/commit/c5dae28b1fb87370385e249ad4eddafdacfa1781))
* **settings:** implemented default settings state ([1b1f825](https://github.com/AniMathIO/ManimStudio/commit/1b1f8251c9018a60056f39f13865494840969865))
* **settings:** implemented settings loading and theme loading ([fa8dcff](https://github.com/AniMathIO/ManimStudio/commit/fa8dcfff9780f1b86de74c89f5bc16b118bda706))
* **themes:** implement catppuccin theme ([18fe02b](https://github.com/AniMathIO/ManimStudio/commit/18fe02b34e156a1df5775d5d50ea303c0f8aa8a4))
* **themes:** implemented first dark and light mode theme ([fbb7cba](https://github.com/AniMathIO/ManimStudio/commit/fbb7cba2c2516170393898ada13c3cab48fe5e50))
* **themes:** refactored global stylesheets with custom signal ([62bae89](https://github.com/AniMathIO/ManimStudio/commit/62bae89fee451e279db025b5cbaf22ab632b74f4))
* **themes:** updated code, to refresh the image path on certain light mode themes ([7e037d3](https://github.com/AniMathIO/ManimStudio/commit/7e037d348d1245d571fbffea5ec54990e97f3644))
* updating README.md about project archiving ([7db997d](https://github.com/AniMathIO/ManimStudio/commit/7db997d7a050ac691b89183bfe2b37acd990153c))
* **videoeditor:** implemented wrapper qmainwindow with settings button ([5119a84](https://github.com/AniMathIO/ManimStudio/commit/5119a843a1da0ff666d21e0a69825f7958817f34))
* **videoeditor:** started the implementation ([4ecfaee](https://github.com/AniMathIO/ManimStudio/commit/4ecfaee82db39dc2d491b75bb9a294ec54e993df))


### Bug Fixes

* **app:** fixed UI errors for resizing the windows without its contents correctly ([b3adb3e](https://github.com/AniMathIO/ManimStudio/commit/b3adb3e08dee4f3e2f5d856d4c5fc9c3eaea4d40))
* **app:** removing unnecessary event that caused exception ([5684ee5](https://github.com/AniMathIO/ManimStudio/commit/5684ee5154c6cb1209d5c05577cc7e417137bea3))
* **ci/cd:** fix docmentation building action ([43e09ef](https://github.com/AniMathIO/ManimStudio/commit/43e09ef61c879476703a3cccfb5268b14cdc67d6))
* **ci/cd:** fixed secret name ([269d9d2](https://github.com/AniMathIO/ManimStudio/commit/269d9d2e35d0dfc968bc7dd84cd8cbd5bfe2ec32))
* **ci/cd:** working on ci/cd fix ([c913bd1](https://github.com/AniMathIO/ManimStudio/commit/c913bd14bdd9b6983b1ab3ac8f170fc521863668))
* **ci/cd:** working on ci/cd system dependency fix ([5cbd76a](https://github.com/AniMathIO/ManimStudio/commit/5cbd76a8ec83197fcf8d6e8c3d7887acdabcc88e))
* **docs:** fixed auto generation for documentation ([d06679d](https://github.com/AniMathIO/ManimStudio/commit/d06679d20a5b89198009b8c7ac641d341b220b2b))
* **docs:** fixed logo order in documentation ([d7de0cd](https://github.com/AniMathIO/ManimStudio/commit/d7de0cd2514da5be7f6954c4222f6d121f4f6404))
* **docs:** fixed typo ([3dd8562](https://github.com/AniMathIO/ManimStudio/commit/3dd856220b01c97befcaac1cdae6d33790cab7c3))
* **docs:** fixing github pages ([93952a6](https://github.com/AniMathIO/ManimStudio/commit/93952a60e9dd982c042f580ddca3c8ac6df7d739))
* **docs:** fixing sphinx errors ([3adcee1](https://github.com/AniMathIO/ManimStudio/commit/3adcee1b8c292af1090705d625571931d2daa7d8))
* **docs:** publish directory location path ([1f41c31](https://github.com/AniMathIO/ManimStudio/commit/1f41c3157ba3251c8de0bfadac4d3d88aa92ba1a))
* **docs:** trying to fix autodoc generation ([f92a1bb](https://github.com/AniMathIO/ManimStudio/commit/f92a1bb5b8aeab9650bdf5bc6c6ae7457eb3acc3))
* **docs:** trying to fix autodoc generation ([f785926](https://github.com/AniMathIO/ManimStudio/commit/f78592602fe41a9cf232b81f731f61297526553f))
* **docs:** trying to fix autodoc problems ([5ea88c9](https://github.com/AniMathIO/ManimStudio/commit/5ea88c9a07b7fe2c6544ad68ca1b4253de1ae749))
* **docs:** trying to fix empty documentation problem ([966918c](https://github.com/AniMathIO/ManimStudio/commit/966918ca3b9c89591dcfbfb9b2cb55d7472e66de))
* **docs:** trying to fix Sphinx autodoc ([0d6e156](https://github.com/AniMathIO/ManimStudio/commit/0d6e1569b5e66e6de0bae28b915f820897f1bc91))
* **docs:** trying to fix the documentation log problem ([3d4ff7e](https://github.com/AniMathIO/ManimStudio/commit/3d4ff7e17281700238eed0e8365f4cfa3a84a9c0))
* **docs:** updated favicon logo name in documentation ([285ca57](https://github.com/AniMathIO/ManimStudio/commit/285ca572e1b1f25a5b12932d8daf4e2f7549e1ef))
* **docs:** working on dependency errors ([21ff47a](https://github.com/AniMathIO/ManimStudio/commit/21ff47a4a3f951d73d3a77af892ecffb3c842b6a))
* **docs:** working on documentation fix ([276ee12](https://github.com/AniMathIO/ManimStudio/commit/276ee12d7f01b000c73224003bc1b3e9e5e3e48c))
* **docs:** working on documentation generation fix ([b502afd](https://github.com/AniMathIO/ManimStudio/commit/b502afd6241d3e3b468a3180a349e5e4301a3c7f))
* **docs:** working on project building problems ([4ef1b5e](https://github.com/AniMathIO/ManimStudio/commit/4ef1b5efce80c978ad6521b6856cb6ed47c89b37))
