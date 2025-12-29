'use client';

import { Globe2, Mail, Sparkles } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useState } from "react";

export default function Page() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('loading');

    try {
      const formData = new FormData();
      formData.append('email', email);

      const response = await fetch('/api/subscribe', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setStatus('success');
        setMessage('Thank you! We\'ll notify you when we launch.');
        setEmail('');
      } else {
        setStatus('error');
        setMessage(data.error || 'Something went wrong. Please try again.');
      }
    } catch (error) {
      setStatus('error');
      setMessage('Failed to submit. Please try again.');
    }
  };
  return (
    <main className="relative isolate min-h-screen overflow-hidden bg-gradient-to-b from-slate-50 via-white to-slate-50">
      {/* Animated background */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(139,92,246,0.15),transparent_40%),radial-gradient(circle_at_80%_80%,rgba(56,189,248,0.15),transparent_40%)]" />
        <div className="absolute left-1/4 top-1/4 h-96 w-96 animate-pulse rounded-full bg-purple-200/20 blur-3xl" />
        <div className="absolute right-1/4 bottom-1/4 h-96 w-96 animate-pulse rounded-full bg-sky-200/20 blur-3xl delay-1000" />
      </div>

      {/* Header */}
      <header className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-8 lg:px-8">
        <div className="flex items-center">
          <Image
            src="/sagatoy_newlogo_ps.png"
            alt="Sagatoy - Born in Gothenburg, Sweden"
            width={1536}
            height={1536}
            className="h-32 w-32"
            priority
            unoptimized
          />
        </div>

        {/* Right side - CTA Button */}
        <div className="flex items-center gap-6">
          <a
            href="#waitlist"
            className="hidden sm:inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-saga-purple to-saga-sky px-6 py-2.5 text-sm font-semibold text-white shadow-lg transition hover:scale-105 hover:shadow-xl"
          >
            <Mail className="h-4 w-4" />
            Join Waitlist
          </a>
        </div>
      </header>

      {/* Main Content */}
      <section className="mx-auto max-w-7xl px-6 lg:px-8 py-12">
        <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
          {/* Left Column - Hero */}
          <div className="space-y-8">
            <h1 className="font-display text-5xl font-bold leading-tight text-saga-ink lg:text-6xl">
              Your Child&apos;s
              <br />
              <span className="bg-gradient-to-r from-saga-purple to-saga-sky bg-clip-text text-transparent">
                AI Companion
              </span>
            </h1>

            <p className="text-xl leading-relaxed text-slate-600">
              An intelligent toy that speaks 5 Nordic languages. No screens, just pure conversational magic for kids aged 4-12.
            </p>

            {/* Key Benefits Cards */}
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="glass rounded-2xl p-6 border border-white/60 shadow-lg hover:shadow-xl transition">
                <div className="text-3xl mb-3">🗣️</div>
                <h3 className="font-semibold text-saga-purple mb-2">Natural Conversation</h3>
                <p className="text-sm text-slate-600">Talks like a real friend, not a robot</p>
              </div>
              <div className="glass rounded-2xl p-6 border border-white/60 shadow-lg hover:shadow-xl transition">
                <div className="text-3xl mb-3">🌍</div>
                <h3 className="font-semibold text-saga-sky mb-2">5 Nordic Languages</h3>
                <p className="text-sm text-slate-600">Swedish, Danish, Norwegian, Finnish, English</p>
              </div>
              <div className="glass rounded-2xl p-6 border border-white/60 shadow-lg hover:shadow-xl transition">
                <div className="text-3xl mb-3">📱❌</div>
                <h3 className="font-semibold text-saga-purple mb-2">100% Screen-Free</h3>
                <p className="text-sm text-slate-600">Zero screen time, better for eyes and sleep</p>
              </div>
              <div className="glass rounded-2xl p-6 border border-white/60 shadow-lg hover:shadow-xl transition">
                <div className="text-3xl mb-3">📚</div>
                <h3 className="font-semibold text-saga-sky mb-2">Story Creation</h3>
                <p className="text-sm text-slate-600">Personalized bedtime stories on demand</p>
              </div>
            </div>

            {/* Status Badge */}
            <div className="glass inline-flex items-center gap-3 rounded-2xl border border-white/60 bg-white/90 px-6 py-3 shadow-lg backdrop-blur">
              <div className="flex h-3 w-3 items-center justify-center">
                <span className="absolute inline-flex h-3 w-3 animate-ping rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex h-2 w-2 rounded-full bg-green-500"></span>
              </div>
              <div>
                <p className="text-sm font-semibold text-saga-ink">Coming Soon</p>
                <p className="text-xs text-slate-500">Launching Q2 2026</p>
              </div>
            </div>

            {/* Email Signup */}
            <div id="waitlist" className="space-y-3 scroll-mt-20">
              <p className="text-sm font-medium text-slate-700">Join the waitlist:</p>
              <form onSubmit={handleSubmit} className="flex max-w-lg gap-3">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="your@email.com"
                  required
                  disabled={status === 'loading'}
                  className="flex-1 rounded-full border-2 border-slate-200 bg-white px-6 py-3 text-sm transition focus:border-saga-purple focus:outline-none disabled:opacity-50"
                />
                <button
                  type="submit"
                  disabled={status === 'loading'}
                  className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-saga-purple to-saga-sky px-8 py-3 font-semibold text-white shadow-lg transition hover:scale-105 hover:shadow-xl disabled:opacity-50 disabled:hover:scale-100"
                >
                  <Mail className="h-4 w-4" />
                  {status === 'loading' ? 'Sending...' : 'Notify Me'}
                </button>
              </form>
              {message && (
                <p className={`text-sm ${status === 'success' ? 'text-green-600' : 'text-red-600'}`}>
                  {message}
                </p>
              )}
              <p className="text-xs text-slate-500">
                We respect your privacy. Unsubscribe at any time.
              </p>
            </div>
          </div>

          {/* Right Column - Product Image */}
          <div className="relative">
            <div className="glass relative overflow-hidden rounded-3xl p-8 shadow-2xl">
              <div className="absolute -right-12 -top-12 h-48 w-48 rounded-full bg-gradient-to-br from-saga-purple/20 to-transparent blur-2xl" />
              <div className="absolute -bottom-12 -left-12 h-48 w-48 rounded-full bg-gradient-to-tr from-saga-sky/20 to-transparent blur-2xl" />

              <div className="relative aspect-square overflow-hidden rounded-2xl bg-gradient-to-br from-slate-100 to-slate-50">
                <Image
                  src="/sagatoy.jpeg"
                  alt="Sagatoy AI companion"
                  fill
                  className="object-cover"
                  priority
                />
              </div>

              {/* Floating badges */}
              <div className="absolute right-4 top-4 rounded-2xl border border-white/60 bg-white/90 px-4 py-3 shadow-lg backdrop-blur">
                <div className="flex items-center gap-2">
                  <Globe2 className="h-5 w-5 text-saga-sky" />
                  <span className="text-sm font-semibold text-saga-ink">5 Languages</span>
                </div>
              </div>

              <div className="absolute left-4 bottom-4 rounded-2xl border border-white/60 bg-white/90 px-4 py-3 shadow-lg backdrop-blur">
                <div className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-saga-purple" />
                  <span className="text-sm font-semibold text-saga-ink">AI Powered</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer - Simple */}
      <footer className="border-t border-slate-200 mt-16 bg-transparent">
        <div className="mx-auto max-w-7xl px-6 py-8 lg:px-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-6">
            <Image
              src="/sagatoy_newlogo_ps.png"
              alt="Sagatoy"
              width={1536}
              height={1536}
              className="h-20 w-20"
              unoptimized
            />

            <div className="text-center sm:text-right text-sm text-slate-500">
              <p>© {new Date().getFullYear()} Sagatoy. Born in Gothenburg, Sweden 🇸🇪</p>
            </div>
          </div>
        </div>
      </footer>
    </main>
  );
}
