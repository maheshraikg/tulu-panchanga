import 'dart:io';

import 'package:flutter_test/flutter_test.dart';

/// Guards against Android resource mistakes that only crash release builds.
void main() {
  const res = 'android/app/src/main/res';

  test('launch screen bitmaps are plain drawables, not the adaptive icon', () {
    // On Android 8+ @mipmap/ic_launcher is an <adaptive-icon> XML; a
    // <bitmap> of it throws Resources$NotFoundException in
    // FlutterActivity.onCreate and the app crashes before it opens.
    final files = Directory(res)
        .listSync(recursive: true)
        .whereType<File>()
        .where((f) => f.path.endsWith('launch_background.xml'))
        .toList();
    expect(files, isNotEmpty);
    for (final f in files) {
      final xml = f.readAsStringSync();
      for (final m in RegExp(r'<bitmap[^>]*>').allMatches(xml)) {
        expect(m[0], isNot(contains('@mipmap/')), reason: f.path);
      }
    }
  });

  test('notification icon exists in every density', () {
    for (final dpi in ['mdpi', 'hdpi', 'xhdpi', 'xxhdpi', 'xxxhdpi']) {
      expect(
        File('$res/drawable-$dpi/ic_stat_panchanga.png').existsSync(),
        isTrue,
        reason: dpi,
      );
      expect(
        File('$res/drawable-$dpi/launch_icon.png').existsSync(),
        isTrue,
        reason: dpi,
      );
    }
  });
}
