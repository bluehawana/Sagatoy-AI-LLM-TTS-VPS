import { ArrowRight, Mail, Sparkles } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

export default function Page() {
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
        <Link
          href="/info"
          className="text-sm font-medium text-slate-700 hover:text-saga-purple transition"
        >
          Learn More
        </Link>
      </header>

      {/* Main Content - Centered */}
      <section className="mx-auto flex min-h-[80vh] max-w-4xl items-center justify-center px-6 lg:px-8">
        <div className="text-center space-y-12">
          {/* Hero */}
          <div className="space-y-6">
            <h1 className="font-display text-6xl font-bold leading-tight text-saga-ink lg:text-7xl">
              Your Child&apos;s
              <br />
              <span className="bg-gradient-to-r from-saga-purple to-saga-sky bg-clip-text text-transparent">
                AI Companion
              </span>
            </h1>

            <p className="text-xl leading-relaxed text-slate-600 max-w-2xl mx-auto">
              An intelligent toy that speaks 5 Nordic languages. No screens, just pure conversational magic for kids aged 4-12.
            </p>
          </div>

          {/* Key Benefits - 3 Simple Points */}
          <div className="grid gap-8 md:grid-cols-3 max-w-3xl mx-auto">
            <div className="space-y-2">
              <div className="text-4xl">🗣️</div>
              <p className="font-semibold text-saga-purple">Natural Conversation</p>
              <p className="text-sm text-slate-600">Talks like a real friend</p>
            </div>
            <div className="space-y-2">
              <div className="text-4xl">🌍</div>
              <p className="font-semibold text-saga-sky">5 Languages</p>
              <p className="text-sm text-slate-600">Nordic + English</p>
            </div>
            <div className="space-y-2">
              <div className="text-4xl">📱❌</div>
              <p className="font-semibold text-saga-purple">Screen-Free</p>
              <p className="text-sm text-slate-600">Zero screen time</p>
            </div>
          </div>

          {/* Status Badge */}
          <div className="glass inline-flex items-center gap-3 rounded-2xl border border-white/60 bg-white/90 px-8 py-4 shadow-lg backdrop-blur">
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
          <div className="space-y-4">
            <p className="text-sm font-medium text-slate-700">Join the waitlist:</p>
            <form className="flex max-w-md mx-auto gap-3">
              <input
                type="email"
                placeholder="your@email.com"
                className="flex-1 rounded-full border-2 border-slate-200 bg-white px-6 py-4 text-sm transition focus:border-saga-purple focus:outline-none"
              />
              <button
                type="submit"
                className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-saga-purple to-saga-sky px-8 py-4 font-semibold text-white shadow-lg transition hover:scale-105 hover:shadow-xl"
              >
                <Mail className="h-4 w-4" />
                Notify Me
              </button>
            </form>
            <p className="text-xs text-slate-500">
              We respect your privacy. Unsubscribe at any time.
            </p>
          </div>

          {/* Learn More Link */}
          <Link
            href="/info"
            className="inline-flex items-center gap-2 text-saga-purple font-medium hover:gap-3 transition-all"
          >
            Discover all features and details
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>

      {/* Footer - Simple */}
      <footer className="border-t border-slate-200 mt-16 bg-transparent">
        <div className="mx-auto max-w-7xl px-6 py-8 lg:px-8">
          <div className="flex flex-col items-center gap-6">
            <Image
              src="/sagatoy_newlogo_ps.png"
              alt="Sagatoy"
              width={1536}
              height={1536}
              className="h-24 w-24"
              unoptimized
            />

            <div className="text-center text-sm text-slate-500">
              <p>© {new Date().getFullYear()} Sagatoy. Born in Gothenburg, Sweden 🇸🇪</p>
            </div>
          </div>
        </div>
      </footer>
    </main>
  );
}
