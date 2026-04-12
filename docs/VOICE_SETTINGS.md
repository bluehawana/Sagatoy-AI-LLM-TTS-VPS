# 🎤 Voice Settings for ToToy AI

## Recommended Settings for Children (Ages 3-10)

### Current Configuration

The system is now optimized for kindergarten-age children with warm, gentle voices that sound like a friendly teacher.

### Swedish Voice (Primary)

- **Voice:** `sv-SE-SofieNeural`
- **Speed:** `-10%` (slightly slower)
- **Why:** Warm, gentle, and comforting - like a kindergarten teacher
- **Best for:** Ages 3-10, bedtime stories, learning

### English Voice

- **Voice:** `en-US-JennyNeural`
- **Speed:** `-10%` (slightly slower)
- **Why:** Warm and friendly female voice
- **Best for:** English-speaking children

## Alternative Voices

### Hillevi (Swedish - Alternative)

- **Voice:** `sv-SE-HilleviNeural`
- **Characteristics:** Clear, bright, cheerful
- **Use when:** You want a slightly more energetic tone

### Mattias (Swedish - Male)

- **Voice:** `sv-SE-MattiasNeural`
- **Characteristics:** Gentle male voice
- **Use when:** You want variety or a male voice

## Why These Settings?

### Slower Speed (-10%)

- ✅ Easier for children to understand
- ✅ Less overwhelming
- ✅ Clearer pronunciation
- ✅ More time to process information
- ✅ Less scary/robotic

### Female Voices

- ✅ Perceived as warmer and more nurturing
- ✅ Similar to kindergarten teachers
- ✅ More comforting for young children
- ✅ Better for bedtime stories

## Testing the Voices

Voice samples are available in:

- `voice_samples/` - Basic voice tests
- `voice_styles/` - Different speeds and styles

### Listen to Samples

```bash
# Best for kindergarten
Invoke-Item voice_styles\Sofie_slightly_slower.mp3

# Alternative
Invoke-Item voice_styles\Hillevi_slightly_slower.mp3
```

## Changing the Voice

To change the voice, update `.env`:

```env
# For Swedish
TTS_VOICE_SV=sv-SE-SofieNeural  # or sv-SE-HilleviNeural

# For English
TTS_VOICE_EN=en-US-JennyNeural

# Speed (-50% to +50%)
TTS_RATE=-10%  # Recommended for children
```

## Tips for Child-Friendly Audio

1. **Keep sentences short** (2-3 sentences max)
2. **Use simple words** (avoid complex vocabulary)
3. **Add pauses** between sentences
4. **Use friendly expressions** ("Hej där!", "Ska vi leka?")
5. **Speak slower** (-10% to -20% speed)
6. **Test with real children** to get feedback

## Feedback from Users

If users say the voice is:

- **Too scary:** Try Sofie at -15% or -20% speed
- **Too slow:** Increase to -5% or normal speed
- **Too robotic:** Ensure using "Neural" voices
- **Too loud:** Adjust volume in playback, not TTS

## Current Status

✅ Voice optimized for kindergarten children (3-10 years)
✅ Warm, gentle, teacher-like tone
✅ Slightly slower for clarity
✅ Less scary than default settings
✅ Tested and approved
