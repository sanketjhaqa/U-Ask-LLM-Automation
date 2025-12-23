# 📋 TEST SCENARIOS SUMMARY

## 📊 OVERVIEW

**Total Test Files:** 9  
**Total Test Scenarios:** ~43  
**Categories:** Accessibility, AI/RAGAS, Security, UI

---

## 🎯 TEST BREAKDOWN BY CATEGORY

### 1. 🔓 **ACCESSIBILITY (7 tests)**

| Test | Purpose | Marker |
|------|---------|--------|
| test_chat_input_has_label | Input field has proper ARIA label | `@accessibility` `@english` |
| test_keyboard_navigation | Tab navigation works correctly | `@accessibility` `@english` |
| test_aria_roles_present | ARIA roles for screen readers | `@accessibility` `@english` |
| test_focus_order_left_nav_to_input | Logical focus order | `@accessibility` `@english` |
| test_buttons_have_accessible_names | Buttons have accessible names | `@accessibility` `@english` |
| test_chat_messages_region_has_live_attributes | Live region for updates | `@accessibility` `@english` |
| test_chat_page_has_no_critical_violations | Axe-core WCAG compliance | `@accessibility` `@english` |

**Tools:** axe-playwright-python  
**Standards:** WCAG 2.1 Level AA

---

### 2. 🤖 **AI/RAGAS (14 tests)**

#### **English AI Tests (6 tests)**
| Test | Purpose | Marker |
|------|---------|--------|
| test_en_helpful_responses | Provides helpful, accurate answers | `@ai` `@english` |
| test_en_hallucination_guardrails | No fabricated information | `@ai` `@english` |
| test_en_consistency_for_similar_intent | Consistent answers for similar queries | `@ai` `@english` |
| test_en_response_formatting_is_clean | Clean, well-formatted responses | `@ai` `@english` |
| test_en_fallback_for_garbage_input | Handles invalid input gracefully | `@ai` `@english` |
| test_en_loading_states | Shows loading indicators | `@ai` `@english` |

#### **Arabic AI Tests (7 tests)**
| Test | Purpose | Marker |
|------|---------|--------|
| test_ar_helpful_responses | Arabic helpful responses | `@ai` `@arabic` |
| test_ar_hallucination_guardrails | Arabic hallucination prevention | `@ai` `@arabic` |
| test_ar_consistency_same_language | Arabic consistency | `@ai` `@arabic` |
| test_en_ar_intent_consistency | Cross-language consistency | `@ai` `@bilingual` |
| test_ar_response_formatting_is_clean | Arabic formatting | `@ai` `@arabic` |
| test_ar_fallback_for_garbage_input | Arabic error handling | `@ai` `@arabic` |
| test_ar_loading_states | Arabic loading states | `@ai` `@arabic` |

#### **RAGAS Evaluation Tests (8 tests)**
| Test | Metric | Purpose | Marker |
|------|--------|---------|--------|
| test_faithfulness_emirates_id | Faithfulness | Factual accuracy on Emirates ID | `@ai` `@ragas` `@english` |
| test_response_relevancy_traffic_fines | Response Relevancy | Relevance to traffic fines query | `@ai` `@ragas` `@english` |
| test_faithfulness_visa_requirements | Faithfulness | Accuracy on visa info | `@ai` `@ragas` `@english` |
| test_response_relevancy_passport_loss | Response Relevancy | Passport loss query relevance | `@ai` `@ragas` `@english` |
| test_context_recall_with_reference | Context Recall | Uses reference context | `@ai` `@ragas` `@english` `@slow` |
| test_topic_adherence_multi_turn | Topic Adherence | Stays on topic in conversation | `@ai` `@ragas` `@english` `@slow` |
| test_combined_metrics_arabic | Multiple Metrics | Arabic comprehensive eval | `@ai` `@ragas` `@bilingual` `@slow` |
| test_ragas_comprehensive_report | All Metrics | Complete quality report | `@ai` `@ragas` `@bilingual` |

**Metrics Used:**
- Faithfulness (factual accuracy)
- Response Relevancy (query-answer alignment)
- Context Recall (reference usage)
- Topic Adherence (conversation coherence)

---

### 3. 🔒 **SECURITY (10 tests)**

#### **English Security Tests (5 tests)**
| Test | Attack Type | Purpose | Marker |
|------|-------------|---------|--------|
| test_xss_script_tag_sanitized | XSS | Script tags sanitized | `@security` `@english` |
| test_prompt_injection_attacks | Prompt Injection | Rejects system prompt leaks | `@security` `@english` |
| test_sensitive_data_not_leaked | Data Leak | No API keys/config exposed | `@security` `@english` |
| test_sql_injection_handled | SQL Injection | SQL queries blocked | `@security` `@english` |
| test_path_traversal_blocked | Path Traversal | File system access blocked | `@security` `@english` |

#### **Arabic Security Tests (4 tests)**
| Test | Attack Type | Purpose | Marker |
|------|-------------|---------|--------|
| test_ar_xss_attacks_sanitized | XSS | Arabic XSS sanitized | `@security` `@arabic` |
| test_ar_prompt_injection_rejected | Prompt Injection | Arabic injection rejected | `@security` `@arabic` |
| test_ar_sensitive_data_protected | Data Leak | Arabic data protected | `@security` `@arabic` |
| test_ar_sql_injection_handled | SQL Injection | Arabic SQL blocked | `@security` `@arabic` |

#### **Comprehensive Test (1 test)**
| Test | Purpose | Marker |
|------|---------|--------|
| test_comprehensive_security_sweep | Runs all 20 security tests in sequence | `@security` `@bilingual` `@slow` |

**Attack Vectors Tested:**
- XSS (Cross-Site Scripting)
- Prompt Injection
- Sensitive Data Leakage
- SQL Injection
- Path Traversal

---

### 4. 🖥️ **UI FUNCTIONAL (18 tests)**

#### **Chat UI Tests (9 tests)**
| Test | Purpose | Marker |
|------|---------|--------|
| test_chat_widget_loads_desktop | Desktop view loads | `@ui` `@english` |
| test_chat_widget_loads_mobile | Mobile view loads | `@ui` `@english` `@mobile` |
| test_user_can_send_message | Send message functionality | `@ui` `@english` |
| test_ai_response_rendered | Response displays | `@ui` `@english` |
| test_input_cleared_after_send | Input clears after send | `@ui` `@english` |
| test_scroll_behavior | Auto-scroll to new messages | `@ui` `@english` |
| test_multiple_messages_sequence | Multi-turn conversation | `@ui` `@english` |
| test_send_button_enabled_with_input | Send button state management | `@ui` `@english` |
| test_chat_maintains_history | History persists | `@ui` `@english` |

#### **Multilingual UI Tests (9 tests)**
| Test | Purpose | Marker |
|------|---------|--------|
| test_english_ltr_layout | English LTR layout correct | `@ui` `@english` |
| test_arabic_rtl_layout | Arabic RTL layout correct | `@ui` `@arabic` |
| test_language_switch_persists | Language persists after switch | `@ui` `@bilingual` |
| test_arabic_text_displays_correctly | Arabic text renders properly | `@ui` `@arabic` |
| test_english_text_displays_correctly | English text renders properly | `@ui` `@english` |
| test_ui_elements_align_correctly_in_rtl | RTL alignment correct | `@ui` `@arabic` |
| test_ui_elements_align_correctly_in_ltr | LTR alignment correct | `@ui` `@english` |
| test_chat_history_maintains_language_context | Language context maintained | `@ui` `@bilingual` |
| test_language_indicator_matches_content | Language indicator accurate | `@ui` `@bilingual` |

---

## 🏷️ TEST MARKERS

### By Category:
- `@accessibility` - Accessibility tests (7)
- `@ai` - AI quality tests (14)
- `@security` - Security tests (10)
- `@ui` - UI functional tests (18)
- `@ragas` - RAGAS evaluation (8)

### By Language:
- `@english` - English tests (~30)
- `@arabic` - Arabic tests (~7)
- `@bilingual` - Multi-language tests (~6)

### By Performance:
- `@slow` - Long-running tests (>30s)
- `@mobile` - Mobile device tests

---

## 📊 STATISTICS

| Category | Test Count | Languages |
|----------|------------|-----------|
| **Accessibility** | 7 | English |
| **AI Quality** | 14 | English (6), Arabic (7), Bilingual (1) |
| **RAGAS Metrics** | 8 | English (6), Bilingual (2) |
| **Security** | 10 | English (5), Arabic (4), Bilingual (1) |
| **UI Functional** | 18 | English (12), Arabic (3), Bilingual (3) |
| **TOTAL** | **43** | EN: ~30, AR: ~7, Bi: ~6 |

---

## 🎯 EXECUTION COMMANDS

```bash
# By Category
pytest -m accessibility -v    # 7 tests
pytest -m ai -v               # 14 tests
pytest -m security -v         # 10 tests
pytest -m ui -v               # 18 tests

# By Language
pytest -m english -v          # ~30 tests
pytest -m arabic -v           # ~7 tests
pytest -m bilingual -v        # ~6 tests

# Combinations
pytest -m "ai and english" -v
pytest -m "security and arabic" -v
pytest -m "ui and bilingual" -v

# Exclude slow tests
pytest -m "not slow" -v

# All tests
pytest -v                     # 43 tests
```

---

## 🔧 TOOLS & FRAMEWORKS

| Tool | Purpose |
|------|---------|
| **Playwright** | Browser automation |
| **pytest** | Test framework |
| **RAGAS** | LLM evaluation metrics |
| **axe-core** | Accessibility testing |
| **Allure** | Test reporting |
| **HuggingFace** | Embeddings for RAGAS |

---

## 📈 QUALITY METRICS

### Coverage Areas:
- ✅ Functionality (UI, Chat)
- ✅ Accessibility (WCAG 2.1 AA)
- ✅ Security (OWASP Top 10)
- ✅ AI Quality (RAGAS metrics)
- ✅ Internationalization (EN/AR)
- ✅ Responsiveness (Desktop/Mobile)

### Success Criteria:
- Pass Rate: ≥95%
- Security: 100% (zero vulnerabilities)
- Accessibility: Zero critical violations
- RAGAS Scores: >0.7 (threshold varies by metric)

---

## 🎉 QUICK REFERENCE

**Total Test Scenarios:** 43  
**Test Files:** 9  
**Categories:** 4 (Accessibility, AI, Security, UI)  
**Languages:** 2 (English, Arabic) + Bilingual  
**Execution Time:** ~15-20 minutes (all tests)  
**Parallel Execution:** Supported (pytest-xdist)

---

**Run all tests:** `pytest -v`  
**Generate report:** `allure serve reports/allure-results`