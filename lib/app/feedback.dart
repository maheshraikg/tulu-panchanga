import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';

import 'scope.dart';

/// Where suggestions and bug reports go.
const String kSupportEmail = 'maheshraikg@gmail.com';

/// CI passes the run number with --dart-define=BUILD_NUMBER=…
const String kBuildNumber = String.fromEnvironment(
  'BUILD_NUMBER',
  defaultValue: 'dev',
);

enum FeedbackKind { suggestion, bug }

/// The mailto: link for [kind], with the details a report needs.
Uri feedbackUri(FeedbackKind kind, {required String details}) {
  final subject = switch (kind) {
    FeedbackKind.suggestion => 'Tulu Panchanga – Suggestion',
    FeedbackKind.bug => 'Tulu Panchanga – Problem report',
  };
  final prompt = switch (kind) {
    FeedbackKind.suggestion => 'My suggestion:',
    FeedbackKind.bug =>
      'What went wrong (for a wrong date or festival, please say what your '
          'panchanga or priest says):',
  };
  final body = '$prompt\n\n\n\n---\n$details';
  // Spaces must be %20, not '+', for mail apps.
  return Uri.parse(
    'mailto:$kSupportEmail'
    '?subject=${Uri.encodeComponent(subject)}'
    '&body=${Uri.encodeComponent(body)}',
  );
}

/// Opens the email app; if there is none, copies the address instead.
Future<void> sendFeedback(BuildContext context, FeedbackKind kind) async {
  final settings = context.settings, s = context.s;
  final now = DateTime.now();
  final details = [
    'App build: $kBuildNumber',
    'Language: ${settings.lang.name}',
    'Place: ${settings.place.name.en} '
        '(${settings.place.lat.toStringAsFixed(3)}, '
        '${settings.place.lon.toStringAsFixed(3)})',
    'Date: ${now.year}-${_two(now.month)}-${_two(now.day)}',
  ].join('\n');
  final messenger = ScaffoldMessenger.of(context);
  var opened = false;
  try {
    opened = await launchUrl(
      feedbackUri(kind, details: details),
      mode: LaunchMode.externalApplication,
    );
  } catch (_) {}
  if (opened) return;
  await Clipboard.setData(const ClipboardData(text: kSupportEmail));
  messenger.showSnackBar(
    SnackBar(content: Text('${s.noEmailApp} $kSupportEmail')),
  );
}

String _two(int n) => n.toString().padLeft(2, '0');
