# Requirements Document

## Introduction

Sagatoyai is an AI-powered plush toy platform designed for the Swedish and EU market. The system embeds AI capabilities into traditional plush toys, enabling natural voice conversations with children. The platform consists of embedded hardware (motherboard, speaker, dual 18650 batteries) inside toys that communicate with self-hosted backend services (LLM and TTS) running on a VPS. The primary language is English, with core features including weather queries, storytelling, singing songs, and educational Q&A (math, general knowledge).

## Glossary

- **Sagatoyai**: The complete AI toy platform including hardware and software components
- **Toy Device**: The physical plush toy containing embedded electronics (motherboard, microphone, speaker, batteries)
- **Backend Server**: Self-hosted VPS services handling LLM inference and TTS generation
- **LLM (Large Language Model)**: AI model that processes user queries and generates conversational responses
- **TTS (Text-to-Speech)**: Service that converts text responses into natural-sounding audio
- **STT (Speech-to-Text)**: Service that converts user voice input into text for processing
- **Wake Word**: A specific phrase that activates the toy's listening mode
- **Session**: A continuous interaction period between a child and the toy

## Requirements

### Requirement 1: Voice Input Processing

**User Story:** As a child, I want to talk to my toy naturally, so that I can ask questions and have conversations without pressing buttons.

#### Acceptance Criteria

1. WHEN the Toy Device detects the wake word THEN the Sagatoyai system SHALL activate listening mode and provide audio feedback within 500 milliseconds
2. WHEN the Toy Device is in listening mode THEN the Sagatoyai system SHALL capture audio input until 2 seconds of silence is detected
3. WHEN audio input is captured THEN the Sagatoyai system SHALL transmit the audio to the Backend Server for STT processing
4. WHEN the STT service receives audio THEN the Backend Server SHALL convert the audio to text with a minimum accuracy of 90% for clear child speech in English
5. IF the STT service fails to process audio THEN the Sagatoyai system SHALL play a friendly error message asking the child to repeat

### Requirement 2: Conversational AI Response

**User Story:** As a child, I want my toy to understand my questions and give helpful answers, so that I can learn and have fun conversations.

#### Acceptance Criteria

1. WHEN the Backend Server receives transcribed text THEN the LLM service SHALL generate a child-appropriate response within 3 seconds
2. WHEN generating responses THEN the LLM service SHALL use language appropriate for children aged 3-10 years
3. WHEN generating responses THEN the LLM service SHALL filter out inappropriate content including violence, adult themes, and harmful information
4. WHEN the user asks a follow-up question THEN the LLM service SHALL maintain conversation context for the current session
5. IF the LLM service cannot generate a response THEN the Backend Server SHALL return a friendly fallback message

### Requirement 3: Text-to-Speech Output

**User Story:** As a child, I want my toy to speak to me in a friendly voice, so that conversations feel natural and engaging.

#### Acceptance Criteria

1. WHEN the Backend Server generates a text response THEN the TTS service SHALL convert the text to audio within 2 seconds
2. WHEN generating speech THEN the TTS service SHALL use a warm, child-friendly voice profile
3. WHEN the Toy Device receives audio data THEN the speaker SHALL play the audio at a safe volume level not exceeding 75 decibels
4. WHEN playing audio THEN the Toy Device SHALL support audio streaming to minimize response latency
5. IF the TTS service fails THEN the Backend Server SHALL return a pre-recorded fallback audio message

### Requirement 4: Weather Information Feature

**User Story:** As a child, I want to ask my toy about the weather, so that I can know if I need to wear a jacket or bring an umbrella.

#### Acceptance Criteria

1. WHEN the user asks about weather THEN the Backend Server SHALL retrieve current weather data for the configured location
2. WHEN presenting weather information THEN the LLM service SHALL describe conditions using child-friendly language and relatable comparisons
3. WHEN weather data includes temperature THEN the Backend Server SHALL present values in Celsius for EU users
4. IF weather service is unavailable THEN the Backend Server SHALL inform the user that weather information is temporarily unavailable

### Requirement 5: Storytelling Feature

**User Story:** As a child, I want my toy to tell me stories, so that I can be entertained and use my imagination.

#### Acceptance Criteria

1. WHEN the user requests a story THEN the LLM service SHALL generate an age-appropriate story between 2-5 minutes in length
2. WHEN generating stories THEN the LLM service SHALL include engaging elements such as characters, conflict, and resolution
3. WHEN the user requests a specific story type THEN the LLM service SHALL adapt the story theme accordingly
4. WHEN telling a story THEN the TTS service SHALL use appropriate pacing and intonation for storytelling
5. WHEN the user asks to continue a story THEN the LLM service SHALL maintain story context and continue the narrative

### Requirement 6: Singing Feature

**User Story:** As a child, I want my toy to sing songs with me, so that I can have fun and learn new songs.

#### Acceptance Criteria

1. WHEN the user requests a song THEN the Backend Server SHALL retrieve or generate child-appropriate song content
2. WHEN playing songs THEN the Toy Device SHALL play pre-recorded audio files for known songs
3. WHEN the user requests an unknown song THEN the LLM service SHALL generate simple, original lyrics and the TTS service SHALL vocalize them
4. WHEN singing THEN the Backend Server SHALL ensure all song content is free from copyright restrictions

### Requirement 7: Educational Q&A Feature

**User Story:** As a child, I want to ask my toy questions about math and other subjects, so that I can learn while playing.

#### Acceptance Criteria

1. WHEN the user asks a math question THEN the LLM service SHALL provide the correct answer with a simple explanation
2. WHEN explaining math concepts THEN the LLM service SHALL use age-appropriate examples and language
3. WHEN the user asks general knowledge questions THEN the LLM service SHALL provide accurate, child-friendly answers
4. WHEN the user asks about inappropriate topics THEN the LLM service SHALL redirect the conversation to appropriate subjects
5. WHEN providing educational content THEN the LLM service SHALL encourage curiosity and further learning

### Requirement 8: Hardware Power Management

**User Story:** As a parent, I want the toy to have long battery life and safe charging, so that my child can play without frequent interruptions.

#### Acceptance Criteria

1. WHILE the Toy Device is powered by dual 18650 batteries THEN the power management system SHALL provide a minimum of 4 hours of active use
2. WHEN battery level falls below 20% THEN the Toy Device SHALL provide an audio notification to the user
3. WHEN battery level falls below 5% THEN the Toy Device SHALL enter low-power mode and notify the user before shutdown
4. WHEN the Toy Device is idle for 5 minutes THEN the power management system SHALL enter sleep mode to conserve battery
5. WHEN the user interacts with a sleeping Toy Device THEN the system SHALL wake within 1 second

### Requirement 9: Network Communication

**User Story:** As a system administrator, I want secure and reliable communication between toys and the server, so that user data is protected and the service is dependable.

#### Acceptance Criteria

1. WHEN the Toy Device communicates with the Backend Server THEN the system SHALL use TLS 1.3 encryption for all data transmission
2. WHEN the Toy Device connects to the Backend Server THEN the system SHALL authenticate using device-specific credentials
3. IF network connectivity is lost THEN the Toy Device SHALL queue requests and retry when connectivity is restored
4. WHEN network latency exceeds 5 seconds THEN the Toy Device SHALL play a waiting message to the user
5. WHEN the Backend Server receives requests THEN the system SHALL validate request authenticity before processing

### Requirement 10: Backend Server Infrastructure

**User Story:** As a system administrator, I want a self-hosted backend that is easy to deploy and maintain, so that I can manage the service efficiently on my VPS.

#### Acceptance Criteria

1. WHEN deploying the Backend Server THEN the system SHALL support containerized deployment using Docker
2. WHEN the Backend Server starts THEN the system SHALL initialize LLM, TTS, and STT services within 60 seconds
3. WHEN handling requests THEN the Backend Server SHALL support a minimum of 10 concurrent toy connections
4. WHEN the Backend Server encounters errors THEN the system SHALL log errors with sufficient detail for debugging
5. WHEN system resources are constrained THEN the Backend Server SHALL gracefully degrade service rather than crash

### Requirement 11: Data Privacy and Safety

**User Story:** As a parent, I want my child's conversations to be private and the toy to be safe, so that I can trust the product with my family.

#### Acceptance Criteria

1. WHEN processing voice data THEN the Backend Server SHALL not store audio recordings beyond the current session
2. WHEN handling user data THEN the system SHALL comply with GDPR requirements for EU users
3. WHEN generating content THEN the LLM service SHALL never request or store personal information from children
4. WHEN the system detects potential safety concerns in conversation THEN the Backend Server SHALL log the event for parental review without storing conversation content
5. WHEN parents request data deletion THEN the Backend Server SHALL remove all associated data within 72 hours

### Requirement 12: API Communication Protocol

**User Story:** As a developer, I want a well-defined API between the toy and server, so that I can maintain and extend the system reliably.

#### Acceptance Criteria

1. WHEN the Toy Device sends requests THEN the system SHALL use a RESTful API with JSON payloads
2. WHEN the Backend Server responds THEN the system SHALL include appropriate HTTP status codes and error messages
3. WHEN transmitting audio data THEN the system SHALL use efficient binary encoding to minimize bandwidth
4. WHEN the API version changes THEN the Backend Server SHALL support backward compatibility for at least one previous version
5. WHEN serializing request and response objects THEN the system SHALL encode them using JSON format
6. WHEN parsing API requests THEN the Backend Server SHALL validate input against the defined JSON schema
