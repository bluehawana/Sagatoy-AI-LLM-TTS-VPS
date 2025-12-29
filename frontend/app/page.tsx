import { ArrowRight, Sparkles, Globe2, Mic, Shield, Languages, Mail } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

const highlights = [
  {
    title: "Voice Activated",
    description: "Natural conversation in Nordic languages",
    icon: <Mic className="h-6 w-6" />
  },
  {
    title: "5 Languages",
    description: "English, Swedish, Danish, Norwegian, Finnish",
    icon: <Languages className="h-6 w-6" />
  },
  {
    title: "Privacy First",
    description: "GDPR compliant, built for Nordic families",
    icon: <Shield className="h-6 w-6" />
  }
];

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
      <header className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-6 lg:px-8">
        <div className="flex items-center gap-3">
          <Image
            src="/logo.svg"
            alt="Sagatoy"
            width={180}
            height={60}
            className="h-14 w-auto"
            priority
          />
        </div>
      </header>

      {/* Main Content */}
      <section className="mx-auto flex min-h-[80vh] max-w-7xl items-center px-6 lg:px-8">
        <div className="grid w-full gap-12 lg:grid-cols-2 lg:items-center">
          {/* Left Column - Hero Content */}
          <div className="space-y-8">
            <div className="inline-flex items-center gap-2 rounded-full border border-saga-purple/20 bg-saga-purple/10 px-4 py-2 text-sm font-semibold text-saga-purple shadow-sm">
              <Globe2 className="h-4 w-4" />
              Coming Soon to Nordic Families
            </div>

            <h2 className="font-display text-5xl font-bold leading-tight text-saga-ink lg:text-6xl">
              AI Companion <br />
              <span className="bg-gradient-to-r from-saga-purple to-saga-sky bg-clip-text text-transparent">
                For Your Child
              </span>
            </h2>

            <p className="text-xl leading-relaxed text-slate-600">
              We&apos;re building something special for kids aged 4-12.
              An intelligent toy companion that speaks Nordic languages and helps children learn through natural conversation.
            </p>

            {/* Status Badge */}
            <div className="glass inline-flex items-center gap-3 rounded-2xl border border-white/60 bg-white/90 px-6 py-4 shadow-lg backdrop-blur">
              <div className="flex h-3 w-3 items-center justify-center">
                <span className="absolute inline-flex h-3 w-3 animate-ping rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex h-2 w-2 rounded-full bg-green-500"></span>
              </div>
              <div>
                <p className="text-sm font-semibold text-saga-ink">Currently in Development</p>
                <p className="text-xs text-slate-500">Launching Q2 2025</p>
              </div>
            </div>

            {/* Email Signup */}
            <div className="space-y-3">
              <p className="text-sm font-medium text-slate-700">Get notified when we launch:</p>
              <form className="flex max-w-md gap-3">
                <input
                  type="email"
                  placeholder="your@email.com"
                  className="flex-1 rounded-full border-2 border-slate-200 bg-white px-5 py-3 text-sm transition focus:border-saga-purple focus:outline-none"
                />
                <button
                  type="submit"
                  className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-saga-purple to-saga-sky px-6 py-3 font-semibold text-white shadow-lg transition hover:scale-105 hover:shadow-xl"
                >
                  <Mail className="h-4 w-4" />
                  Notify Me
                </button>
              </form>
              <p className="text-xs text-slate-500">
                We respect your privacy. Unsubscribe at any time.
              </p>
            </div>
          </div>

          {/* Right Column - Image */}
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

              {/* Floating badge */}
              <div className="absolute right-4 top-4 rounded-2xl border border-white/60 bg-white/90 px-4 py-3 shadow-lg backdrop-blur">
                <div className="flex items-center gap-2">
                  <Globe2 className="h-5 w-5 text-saga-sky" />
                  <span className="text-sm font-semibold text-saga-ink">5 Languages</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Preview */}
      <section className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
        <div className="text-center mb-12">
          <h3 className="font-display text-3xl font-bold text-saga-ink mb-3">
            What to Expect
          </h3>
          <p className="text-lg text-slate-600">
            Follow our updates for the latest news
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {highlights.map((item) => (
            <div key={item.title} className="glass rounded-2xl p-8 text-center transition hover:shadow-xl">
              <div className="mx-auto mb-4 inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-saga-purple to-saga-sky text-white shadow-lg">
                {item.icon}
              </div>
              <h4 className="mb-2 font-display text-xl font-bold text-saga-ink">{item.title}</h4>
              <p className="text-slate-600">{item.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto max-w-7xl px-6 py-8 lg:px-8">
          <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
            <Image
              src="/logo.svg"
              alt="Sagatoy"
              width={150}
              height={50}
              className="h-10 w-auto"
            />

            <div className="flex items-center gap-6 text-sm text-slate-600">
              <Link href="mailto:hello@sagatoy.com" className="hover:text-saga-purple transition">
                Contact
              </Link>
              <span className="text-xs text-slate-400">Made with ❤️ in Sweden</span>
            </div>
          </div>

          <div className="mt-6 border-t border-slate-200 pt-6 text-center text-sm text-slate-500">
            <p>© {new Date().getFullYear()} Sagatoy. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </main>
  );
}
