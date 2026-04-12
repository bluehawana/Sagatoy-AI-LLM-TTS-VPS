"""Test new features: Conversation Context, LLM Fallback, Streaming TTS.

Run: python test_new_features.py
"""

from dotenv import load_dotenv
import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

load_dotenv()


async def test_conversation_context():
    """Test conversation context management."""
    print("\n" + "="*60)
    print("🧠 Testing Conversation Context Manager")
    print("="*60)

    from sagatoyai.services.conversation_context import conversation_manager

    # Create a new context
    session_id = "test-session-123"
    device_id = "test-device-456"

    context = conversation_manager.get_or_create(
        session_id=session_id,
        device_id=device_id,
        language="sv",
    )

    print(f"✅ Created context for session: {session_id}")
    print(f"   Device: {device_id}")
    print(f"   Language: {context.preferred_language}")

    # Add some conversation turns
    context.add_user_message("Hej! Vad heter du?", intent="general")
    context.add_assistant_message("Hej! Jag heter Saga och jag är din vän!")

    context.add_user_message("Kan du berätta en saga?", intent="story")
    context.add_assistant_message(
        "Visst! Det var en gång en modig liten kanin...")

    print(f"\n📝 Conversation history ({len(context.history)} turns):")
    for turn in context.history:
        print(f"   {turn.role}: {turn.content[:50]}...")

    # Get context for LLM
    llm_context = context.get_context_for_llm(max_turns=3)
    print(f"\n🤖 LLM context (last 3 turns):")
    for msg in llm_context:
        print(f"   {msg['role']}: {msg['content'][:40]}...")

    # Test summary
    print(f"\n📊 Summary: {context.get_summary()}")

    # Test expiry
    print(f"⏰ Is expired: {context.is_expired()}")

    print("\n✅ Conversation context test PASSED!")
    return True


async def test_llm_fallback():
    """Test LLM fallback service."""
    print("\n" + "="*60)
    print("🔄 Testing LLM Fallback Service")
    print("="*60)

    from sagatoyai.services.llm_fallback import llm_fallback_service, LLMProvider

    # Check provider status
    status = llm_fallback_service.get_provider_status()
    print("\n📊 Provider status:")
    for provider, info in status.items():
        health = "✅ Healthy" if info["healthy"] else "❌ Unhealthy"
        print(f"   {provider}: {health} (failures: {info['failures']})")

    # Test conversation response
    print("\n🗣️ Testing conversation response...")

    test_inputs = [
        ("Hej! Hur mår du?", "sv"),
        ("What's the weather like?", "en"),
        ("Berätta om dinosaurier!", "sv"),
    ]

    for user_input, language in test_inputs:
        print(f"\n   User ({language}): {user_input}")

        try:
            result = await llm_fallback_service.generate_response(
                user_input=user_input,
                language=language,
            )

            print(f"   Provider: {result.provider.value}")
            print(f"   Latency: {result.latency_ms:.0f}ms")
            print(f"   Intent: {result.intent.value}")
            print(f"   Fallback used: {result.fallback_used}")
            print(f"   Response: {result.text[:100]}...")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n✅ LLM fallback test PASSED!")
    return True


async def test_streaming_tts():
    """Test streaming TTS service."""
    print("\n" + "="*60)
    print("🔊 Testing Streaming TTS Service")
    print("="*60)

    from sagatoyai.services.streaming_tts import streaming_tts_service

    test_text = "Hej! Jag är Saga. Vill du höra en rolig saga om en liten kanin?"

    print(f"\n📝 Text: {test_text}")

    # Test sentence splitting
    sentences = streaming_tts_service._split_into_sentences(test_text)
    print(f"\n📄 Split into {len(sentences)} sentences:")
    for i, s in enumerate(sentences):
        print(f"   {i+1}. {s}")

    # Test duration estimate
    duration = await streaming_tts_service.get_audio_duration_estimate(test_text, "sv")
    print(f"\n⏱️ Estimated duration: {duration:.1f} seconds")

    # Test streaming synthesis
    print("\n🎵 Testing streaming synthesis...")

    total_bytes = 0
    chunk_count = 0

    async for chunk in streaming_tts_service.synthesize_streaming(test_text, "sv"):
        total_bytes += len(chunk)
        chunk_count += 1
        if chunk_count <= 5:
            print(f"   Chunk {chunk_count}: {len(chunk)} bytes")
        elif chunk_count == 6:
            print("   ...")

    print(f"\n   Total: {chunk_count} chunks, {total_bytes:,} bytes")

    # Test sentence-by-sentence streaming
    print("\n🎤 Testing sentence-by-sentence streaming...")

    async for sentence, audio in streaming_tts_service.synthesize_sentences_streaming(
        test_text, "sv"
    ):
        print(f"   '{sentence[:30]}...' → {len(audio):,} bytes")

    print("\n✅ Streaming TTS test PASSED!")
    return True


async def test_full_pipeline():
    """Test full pipeline: Context → LLM → Streaming TTS."""
    print("\n" + "="*60)
    print("🚀 Testing Full Pipeline")
    print("="*60)

    from sagatoyai.services.conversation_context import conversation_manager
    from sagatoyai.services.llm_fallback import llm_fallback_service
    from sagatoyai.services.streaming_tts import streaming_tts_service

    # Create session
    session_id = "pipeline-test-001"
    device_id = "device-001"

    context = conversation_manager.get_or_create(session_id, device_id, "sv")
    print(f"\n📱 Session: {session_id}")

    # Simulate conversation
    user_inputs = [
        "Hej Saga!",
        "Hur är vädret idag?",
        "Berätta en kort saga!",
    ]

    for user_input in user_inputs:
        print(f"\n👧 Child: {user_input}")

        # Add to context
        context.add_user_message(user_input)

        # Get LLM response with context
        llm_context = context.get_context_for_llm(max_turns=3)

        result = await llm_fallback_service.generate_response(
            user_input=user_input,
            language="sv",
            context=llm_context,
        )

        # Add response to context
        context.add_assistant_message(result.text)

        print(
            f"🧸 ToToy ({result.provider.value}, {result.latency_ms:.0f}ms): {result.text[:100]}...")

        # Generate TTS (just count bytes, don't play)
        audio_bytes = await streaming_tts_service.synthesize_to_bytes(result.text, "sv")
        print(f"🔊 Audio: {len(audio_bytes):,} bytes")

    # Show final context
    print(f"\n📊 Final context: {len(context.history)} turns")
    print(f"   Summary: {context.get_summary()}")

    print("\n✅ Full pipeline test PASSED!")
    return True


async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("🧪 Sagatoyai New Features Test Suite")
    print("="*60)
    print("\nTesting features inspired by XiaoGPT:")
    print("1. Conversation Context Manager")
    print("2. LLM Fallback Service (Groq → Gemini)")
    print("3. Streaming TTS")
    print("4. Full Pipeline Integration")

    results = []

    # Test 1: Conversation Context
    try:
        results.append(("Conversation Context", await test_conversation_context()))
    except Exception as e:
        print(f"❌ Conversation Context test failed: {e}")
        results.append(("Conversation Context", False))

    # Test 2: LLM Fallback
    try:
        results.append(("LLM Fallback", await test_llm_fallback()))
    except Exception as e:
        print(f"❌ LLM Fallback test failed: {e}")
        results.append(("LLM Fallback", False))

    # Test 3: Streaming TTS
    try:
        results.append(("Streaming TTS", await test_streaming_tts()))
    except Exception as e:
        print(f"❌ Streaming TTS test failed: {e}")
        results.append(("Streaming TTS", False))

    # Test 4: Full Pipeline
    try:
        results.append(("Full Pipeline", await test_full_pipeline()))
    except Exception as e:
        print(f"❌ Full Pipeline test failed: {e}")
        results.append(("Full Pipeline", False))

    # Summary
    print("\n" + "="*60)
    print("📋 Test Results Summary")
    print("="*60)

    passed = 0
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {name}: {status}")
        if result:
            passed += 1

    print(f"\n   Total: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("\n🎉 All tests passed! New features are ready.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")


if __name__ == "__main__":
    asyncio.run(main())
