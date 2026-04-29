"""NVIDIA NIM Voice Chat Test - EN/SV/ZH benchmark."""

import pytest
import asyncio
import time
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend/src'))

from sagatoyai.services.nim_llm import nim_service


class TestNIMVoiceChat:
    """Test NVIDIA NIM for toy voice chat responses."""

    @pytest.mark.asyncio
    async def test_basic_math(self):
        """Test basic math questions for kids."""
        test_cases = [
            ("en", "2 plus 3 equals what"),
            ("sv", "Vad är 5 plus 3"),
            ("zh", "2加3等于多少"),
        ]
        results = []
        for lang, question in test_cases:
            start = time.time()
            response, intent = await nim_service.generate_conversation_response(
                question, language=lang
            )
            latency = (time.time() - start) * 1000
            results.append((lang, question, response, latency))
            print(f"[{lang}] {question} -> {response[:50]}... ({latency:.0f}ms)")

        assert all(r[3] < 30000 for r in results), "Latency too high"
        assert all(r[2] for r in results), "Empty response"

    @pytest.mark.asyncio
    async def test_ask_for_song(self):
        """Test asking for songs in different languages."""
        test_cases = [
            ("en", "Can you sing me a song"),
            ("sv", "Kan du sjunga en sång för mig"),
            ("zh", "你能给我唱首歌吗"),
        ]
        for lang, question in test_cases:
            response, _ = await nim_service.generate_conversation_response(
                question, language=lang
            )
            print(f"[{lang}] Song request: {response[:80]}...")
            assert len(response) > 10, "Response too short"

    @pytest.mark.asyncio
    async def test_ask_for_story(self):
        """Test asking for stories/sagas."""
        test_cases = [
            ("en", "Tell me a short story"),
            ("sv", "Berätta en saga för mig"),
            ("zh", "给我讲个小故事"),
        ]
        for lang, question in test_cases:
            response, _ = await nim_service.generate_conversation_response(
                question, language=lang
            )
            print(f"[{lang}] Story request: {response[:80]}...")
            assert len(response) > 20, "Story too short"

    @pytest.mark.asyncio
    async def test_basic_questions(self):
        """Test basic questions kids might ask."""
        test_cases = [
            ("en", "What is your name"),
            ("en", "How are you"),
            ("en", "What day is it today"),
            ("sv", "Vad heter du"),
            ("sv", "Hur mår du"),
            ("sv", "Vilken dag är det idag"),
            ("zh", "你叫什么名字"),
            ("zh", "你好吗"),
            ("zh", "今天星期几"),
        ]
        for lang, question in test_cases:
            response, _ = await nim_service.generate_conversation_response(
                question, language=lang
            )
            print(f"[{lang}] {question} -> {response[:60]}...")
            assert len(response) > 5, "Empty response"

    @pytest.mark.asyncio
    async def test_kid_questions_round_9(self):
        """Test questions appropriate for 9-year-old kids."""
        test_cases = [
            ("en", "Why is the sky blue"),
            ("en", "What is the biggest animal"),
            ("en", "Can you tell me a joke"),
            ("sv", "Varför är himlen blå"),
            ("sv", "Vilket är det största djuret"),
            ("sv", "Kan du berätta en rolig historia"),
            ("zh", "为什么天空是蓝色的"),
            ("zh", "最大的动物是什么"),
            ("zh", "你能给我讲个笑话吗"),
        ]
        for lang, question in test_cases:
            start = time.time()
            response, _ = await nim_service.generate_conversation_response(
                question, language=lang
            )
            latency = (time.time() - start) * 1000
            print(f"[{lang}] {question[:30]}... -> {response[:50]}... ({latency:.0f}ms)")
            assert len(response) > 10, "Response too short"

    @pytest.mark.asyncio
    async def test_all_languages_performance(self):
        """Benchmark latency across all supported languages."""
        question = "Hello, how are you today"
        languages = ["en", "sv", "da", "no", "fi", "zh"]

        print("\n=== NIM Latency Benchmark ===")
        results = []
        for lang in languages:
            start = time.time()
            response, _ = await nim_service.generate_conversation_response(
                question, language=lang
            )
            latency = (time.time() - start) * 1000
            results.append((lang, latency))
            print(f"{lang}: {latency:.0f}ms")

        avg_latency = sum(r[1] for r in results) / len(results)
        print(f"Average: {avg_latency:.0f}ms")

        assert avg_latency < 30000, f"Average latency {avg_latency}ms too high"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])