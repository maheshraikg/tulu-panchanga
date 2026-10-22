import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:url_launcher/url_launcher.dart';

import 'scope.dart';

/// Where suggestions and bug reports go.
const String kSupportEmail = 'maheshraikg@gmail.com';

/// Developer's WhatsApp number (country code, digits only) for wa.me links.
const String kWhatsAppNumber = '918105693721';
const String kWhatsAppDisplay = '+91 81056 93721';

/// Shown on Google Play and linked from Settings.
const String kPrivacyPolicyUrl =
    'https://github.com/maheshraikg/tulu-panchanga/blob/main/PRIVACY.md';

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
  final s = context.s;
  final details = _details(context);
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

/// App build, language, place and date, so a report can be reproduced.
String _details(BuildContext context) {
  final settings = context.settings;
  final now = DateTime.now();
  return [
    'App build: $kBuildNumber',
    'Language: ${settings.lang.name}',
    'Place: ${settings.place.name.en} '
        '(${settings.place.lat.toStringAsFixed(3)}, '
        '${settings.place.lon.toStringAsFixed(3)})',
    'Date: ${now.year}-${_two(now.month)}-${_two(now.day)}',
  ].join('\n');
}

/// The wa.me link that opens a WhatsApp chat with the developer.
Uri whatsAppUri({required String details}) => Uri.parse(
  'https://wa.me/$kWhatsAppNumber'
  '?text=${Uri.encodeComponent('Tulu Panchanga:\n\n\n---\n$details')}',
);

/// Opens WhatsApp; if it is not installed, copies the number instead.
Future<void> openWhatsApp(BuildContext context) async {
  final s = context.s, messenger = ScaffoldMessenger.of(context);
  final uri = whatsAppUri(details: _details(context));
  var opened = false;
  try {
    opened = await launchUrl(uri, mode: LaunchMode.externalApplication);
  } catch (_) {}
  if (opened) return;
  await Clipboard.setData(const ClipboardData(text: kWhatsAppDisplay));
  messenger.showSnackBar(
    SnackBar(content: Text('${s.noWhatsApp} $kWhatsAppDisplay')),
  );
}

String _two(int n) => n.toString().padLeft(2, '0');

/// Opens the privacy policy in the browser; if that fails, copies the link.
Future<void> openPrivacyPolicy(BuildContext context) async {
  final s = context.s, messenger = ScaffoldMessenger.of(context);
  var opened = false;
  try {
    opened = await launchUrl(
      Uri.parse(kPrivacyPolicyUrl),
      mode: LaunchMode.externalApplication,
    );
  } catch (_) {}
  if (opened) return;
  await Clipboard.setData(const ClipboardData(text: kPrivacyPolicyUrl));
  messenger.showSnackBar(
    SnackBar(content: Text('${s.linkCopied} $kPrivacyPolicyUrl')),
  );
}
