import 'package:flutter_test/flutter_test.dart';
import 'package:tulu_panchanga/app/feedback.dart';

void main() {
  test('feedback link is a mailto with %20-encoded subject and body', () {
    final uri = feedbackUri(FeedbackKind.bug, details: 'Place: Udupi');
    expect(uri.scheme, 'mailto');
    expect(uri.path, kSupportEmail);
    final raw = uri.toString();
    expect(raw, contains('subject=Tulu%20Panchanga%20%E2%80%93%20Problem'));
    expect(raw, isNot(contains('+')));
    expect(Uri.decodeComponent(raw), contains('Place: Udupi'));
  });

  test('suggestion and bug links have different subjects', () {
    final a = feedbackUri(FeedbackKind.suggestion, details: '');
    final b = feedbackUri(FeedbackKind.bug, details: '');
    expect(a.toString(), contains('Suggestion'));
    expect(b.toString(), contains('Problem%20report'));
  });
}
