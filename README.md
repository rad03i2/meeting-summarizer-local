# Meeting Summarizer Local

A privacy-first Python tool that turns plain-text meeting transcripts into concise extractive summaries, action items, decisions, speaker statistics, and keywords — entirely on your machine.

> **Local by design:** no API keys, cloud service, telemetry, or network access is required.

## English

### Overview
Meeting Summarizer Local is useful when you already have a UTF-8 transcript and want a reproducible first-pass meeting report without sending private conversations to an external service. It uses deterministic text scoring and phrase-based extraction rather than pretending to be a generative AI system.

### Why it exists
Meeting transcripts are often long while the useful follow-up is small: what mattered, what was decided, and who needs to do what. This project provides a lightweight, inspectable baseline that works offline and supports both English and Arabic text.

### Features
- Parses `Speaker: text` transcripts, including optional `[HH:MM]` / `HH:MM` timestamps.
- Extractive overview ranked from the actual transcript; it does not invent sentences.
- Heuristic action-item and decision detection in English and Arabic.
- Speaker utterance counts and frequent keywords.
- Markdown and machine-readable JSON reports.
- UTF-8 and Arabic support.
- CLI plus a small Python API.
- Zero runtime dependencies outside the Python standard library.
- Clear validation for empty input, missing files, invalid limits, and non-UTF-8 transcripts.

### Preview
```text
$ meeting-summary examples/sample-transcript.txt
# Meeting Summary

## Overview
- Lina: Today we need to finalize the dashboard release.
...
## Action items
- Omar: I will run the test suite before Thursday.
```

For screenshots, run the command in your preferred terminal and capture the generated Markdown preview. No graphical interface is included in v1.0.

### Requirements & installation
- Python 3.10 or newer
- pip

```bash
git clone https://github.com/rad03i2/meeting-summarizer-local.git
cd meeting-summarizer-local
python -m pip install -e .
```

For development:
```bash
python -m pip install -e . pytest
```

### Usage
```bash
meeting-summary transcript.txt
meeting-summary transcript.txt --format json
meeting-summary transcript.txt --max-points 7 --keywords 12
meeting-summary transcript.txt --output reports/meeting.md --title "Sprint Review"
python -m meeting_summarizer examples/sample-transcript.txt
meeting-summary --version
```

Recommended transcript form:
```text
[09:00] Alice: We agreed to ship on Friday.
09:03 Bob: I will update the dashboard tomorrow.
Alice: Please include the air-quality metrics.
```
Continuation lines without a speaker are appended to the previous utterance.

Python API:
```python
from meeting_summarizer import summarize

result = summarize("Alice: We agreed to ship Friday.\nBob: I will update the docs.")
print(result.action_items)
print(result.decisions)
print(result.to_dict())
```

### Configuration
There is no configuration file and no environment variable is required. Behavior is controlled explicitly with `--max-points`, `--keywords`, `--format`, `--title`, and `--output`.

### Project structure
```text
src/meeting_summarizer/   Core parser, summarizer, CLI and module entry point
tests/                    Functional tests
examples/                 Safe bilingual sample transcript
.github/workflows/ci.yml  Cross-platform CI
SECURITY.md                Security/privacy model
CONTRIBUTING.md            Contribution guide
```

### Testing
```bash
python -m compileall -q src tests
pytest -q
meeting-summary examples/sample-transcript.txt --format json
```
CI runs these checks on Ubuntu, Windows, and macOS with Python 3.10, 3.12, and 3.13.

### Security & privacy
Transcript text stays local. The application performs no network calls, executes no transcript content, and writes a report only when you explicitly provide `--output`. Do not commit confidential real-world transcripts to source control. See [SECURITY.md](SECURITY.md).

### Limitations
This is deterministic extractive summarization, not semantic or generative understanding. Action/decision detection is phrase-based and can miss implicit commitments or produce false positives. Speaker parsing expects a colon-delimited format. It does not transcribe audio/video, perform diarization, translate text, or verify whether statements are true. Always compare important decisions with the source transcript.

### Optional roadmap
Potential future work includes SRT/VTT import, configurable marker dictionaries, richer sentence segmentation, and an optional local-model adapter. These are not implemented today.

### Contributing & license
See [CONTRIBUTING.md](CONTRIBUTING.md). Licensed under the [MIT License](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
**Meeting Summarizer Local** أداة بايثون محلية تحول النصوص المكتوبة لاجتماعاتك إلى ملخص استخراجي، ومهام متابعة، وقرارات، وإحصاءات للمتحدثين، وكلمات متكررة، من دون إرسال محتوى الاجتماع إلى خدمة خارجية.

### لماذا هذا المشروع؟
قد يكون نص الاجتماع طويلًا بينما المطلوب بعده بسيط: أهم النقاط، القرارات، وما الذي يجب متابعته. يوفر المشروع معالجة محلية قابلة للفحص وإعادة الإنتاج، ويدعم النص العربي والإنجليزي بصيغة UTF-8.

### المزايا
- قراءة صيغة `المتحدث: النص` مع طابع زمني اختياري.
- اختيار نقاط الملخص من نص الاجتماع نفسه بدل إنشاء جمل غير موجودة.
- كشف إرشادي لمهام المتابعة والقرارات بالعربية والإنجليزية.
- إحصاء مداخلات المتحدثين واستخراج الكلمات المتكررة.
- إخراج Markdown أو JSON.
- دعم العربية وUTF-8.
- واجهة أوامر وواجهة Python برمجية صغيرة.
- لا توجد مكتبات تشغيل خارج المكتبة القياسية لبايثون.
- تحقق واضح من الملفات والمدخلات غير الصحيحة.

### معاينة
```bash
meeting-summary examples/sample-transcript.txt
meeting-summary examples/sample-transcript.txt --format json
```
لا توجد واجهة رسومية في الإصدار 1.0؛ يمكن أخذ لقطة من الطرفية أو من معاينة ملف Markdown الناتج عند الحاجة إلى صورة للمستودع.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث وpip:
```bash
git clone https://github.com/rad03i2/meeting-summarizer-local.git
cd meeting-summarizer-local
python -m pip install -e .
```
وللتطوير والاختبارات:
```bash
python -m pip install -e . pytest
```

### الاستخدام
```bash
meeting-summary meeting.txt
meeting-summary meeting.txt --format json
meeting-summary meeting.txt --max-points 7 --keywords 12
meeting-summary meeting.txt -o reports/summary.md --title "اجتماع المشروع"
python -m meeting_summarizer examples/sample-transcript.txt
```

الصيغة المفضلة:
```text
[10:00] علي: نحتاج إنهاء التقرير اليوم.
10:05 سارة: سوف أراجع الجداول غدًا.
علي: اتفق الفريق على اعتماد النسخة الجديدة.
```
والأسطر المستمرة التي لا تبدأ باسم متحدث تُلحق بالمداخلة السابقة.

مثال Python:
```python
from meeting_summarizer import summarize
result = summarize("علي: اتفق الفريق على النشر.\nسارة: سوف أراجع التقرير.")
print(result.action_items)
```

### الإعداد
لا يحتاج المشروع إلى `.env` أو مفاتيح API أو ملف إعداد. يمكن التحكم بعدد نقاط الملخص والكلمات وطريقة الإخراج والعنوان ومسار التقرير من خيارات CLI مباشرة.

### بنية المشروع
```text
src/meeting_summarizer/   المحرك وواجهة الأوامر
tests/                    اختبارات وظيفية
examples/                 مثال آمن ثنائي اللغة
.github/workflows/ci.yml  اختبارات CI متعددة الأنظمة
SECURITY.md                سياسة الأمان والخصوصية
CONTRIBUTING.md            دليل المساهمة
```

### الاختبارات
```bash
python -m compileall -q src tests
pytest -q
meeting-summary examples/sample-transcript.txt --format json
```
ويشغّل CI هذه الفحوص على Ubuntu وWindows وmacOS مع عدة إصدارات من Python.

### الأمان والخصوصية
يبقى نص الاجتماع على الجهاز؛ لا يجري البرنامج اتصالات شبكة، ولا ينفذ محتوى النص، ولا يكتب تقريرًا إلى القرص إلا عند طلب ذلك عبر `--output`. لا ترفع نصوص اجتماعات سرية حقيقية إلى المستودعات العامة. راجع [SECURITY.md](SECURITY.md).

### القيود
هذا ملخص استخراجي حتمي وليس فهمًا دلاليًا أو نموذجًا توليديًا. كشف المهام والقرارات يعتمد على عبارات إرشادية، لذلك قد يفوّت المعاني الضمنية أو ينتج حالات إيجابية خاطئة. لا يحول الصوت أو الفيديو إلى نص، ولا ينفذ فصل المتحدثين أو الترجمة أو التحقق من صحة الأقوال. يجب مراجعة القرارات المهمة مع النص الأصلي.

### تطوير اختياري مستقبلًا
يمكن مستقبلًا إضافة استيراد SRT/VTT، وقواميس علامات قابلة للتخصيص، وتقسيم جمل أكثر تطورًا، ومحول اختياري لنموذج محلي. هذه الميزات غير موجودة حاليًا.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md). المشروع مرخص برخصة [MIT](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
