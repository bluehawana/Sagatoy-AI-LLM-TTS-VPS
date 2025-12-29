import { ArrowRight, CalendarClock, CloudSun, ShieldCheck, Sparkles, Stars } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

const highlights = [
  {
    title: "AI Storytelling",
    body: "Groq + Gemini powered tales tailored for kids 3-10 with Swedish-first voices and softer pacing.",
    icon: <Sparkles className="h-6 w-6 text-saga-purple" />
  },
  {
    title: "Safe & Private",
    body: "GDPR-minded, on-device wake word and secure Rust backend APIs.",
    icon: <ShieldCheck className="h-6 w-6 text-saga-sky" />
  },
  {
    title: "Built for Play",
    body: "ESP32-based plush toy with gentle TTS, weather, and conversation memory.",
    icon: <ArrowRight className="h-6 w-6 text-saga-gold" />
  }
];

const roadmap = [
  { label: "Now", status: "Live VPS + secured APIs on sagatoy.com" },
  { label: "Next", status: "Full landing + parent portal" },
  { label: "Soon", status: "Batch of pilot devices for Swedish families" }
];

const upgrades = [
  {
    title: "Real conversations",
    body: "Wake words (“Hej Saga”), natural back-and-forth, and gentle kid-safe replies.",
    icon: <Stars className="h-5 w-5 text-saga-purple" />
  },
  {
    title: "Weather + date/time",
    body: "Quick answers about the day ahead, perfect before school runs.",
    icon: <CloudSun className="h-5 w-5 text-saga-sky" />
  },
  {
    title: "Storytelling",
    body: "Warm Swedish voices telling original bedtime stories made for ages 3-10.",
    icon: <CalendarClock className="h-5 w-5 text-saga-gold" />
  }
];

export default function Page() {
  return (
    <main className="relative isolate overflow-hidden">
      <div className="absolute inset-0 -z-10">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(139,92,246,0.12),transparent_30%),radial-gradient(circle_at_80%_0%,rgba(56,189,248,0.16),transparent_35%)]" />
      </div>

      <header className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-6">
        <div className="flex items-center gap-3">
          <div className="h-11 w-11 rounded-2xl bg-white shadow-glow ring-1 ring-white/60 flex items-center justify-center">
            <span className="text-xl font-bold text-saga-purple">S</span>
          </div>
          <div>
            <p className="font-display text-xl text-saga-ink">SagaToy</p>
            <p className="text-sm text-slate-500">Magical AI story friend</p>
          </div>
        </div>
        <Link
          href="https://sagatoy.com"
          className="rounded-full bg-saga-purple px-4 py-2 text-sm font-semibold text-white shadow-glow transition hover:-translate-y-0.5 hover:shadow-lg"
        >
          Live on sagatoy.com
        </Link>
      </header>

      <section className="mx-auto flex w-full max-w-6xl flex-col gap-10 px-6 pb-16 pt-4 md:flex-row md:items-center">
        <div className="flex-1 space-y-6">
          <div className="inline-flex items-center gap-2 rounded-full border border-saga-purple/30 bg-white/80 px-3 py-1 text-xs font-semibold text-saga-purple shadow-glow">
            Under construction · Resume link ready
          </div>
          <h1 className="font-display text-4xl leading-tight text-saga-ink sm:text-5xl md:text-6xl">
            Your child&apos;s <span className="text-saga-purple">magical storyteller</span> and curious friend.
          </h1>
          <p className="text-lg leading-relaxed text-slate-600">
            SagaToy blends warm Swedish voices, safe AI responses, and playful hardware into one cozy plush toy. We&apos;re building
            fast—when recruiters and partners search sagatoy.com, they&apos;ll see we&apos;re live and growing.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="mailto:hello@sagatoy.com"
              className="inline-flex items-center gap-2 rounded-full bg-saga-purple px-5 py-3 text-sm font-semibold text-white shadow-glow transition hover:-translate-y-0.5"
            >
              Get early access
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="#roadmap"
              className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-saga-ink transition hover:-translate-y-0.5"
            >
              See what&apos;s coming
            </Link>
          </div>
          <div className="grid gap-3 rounded-2xl border border-white/70 bg-white/90 p-4 shadow-xl backdrop-blur">
            <p className="text-sm font-semibold text-slate-700">We&apos;re shipping with</p>
            <div className="grid grid-cols-2 gap-3 text-sm text-slate-600 sm:grid-cols-4">
              {["Next.js + Tailwind", "Shadcn UI", "Rust backend", "MySQL for parent data"].map((item) => (
                <div key={item} className="rounded-lg border border-slate-100 bg-slate-50 px-3 py-2 text-center">
                  {item}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="flex flex-1 justify-center">
          <div className="glass relative w-full max-w-md rounded-3xl p-6">
            <div className="absolute -left-6 -top-6 rounded-full bg-saga-purple/20 px-3 py-1 text-xs font-semibold text-saga-purple">
              Kids 3-10
            </div>
            <div className="absolute -right-4 top-12 rounded-full bg-saga-gold/20 px-3 py-1 text-xs font-semibold text-saga-gold">
              Bilingual
            </div>
            <div className="relative aspect-[4/5] overflow-hidden rounded-2xl bg-gradient-to-br from-saga-purple/10 via-white to-saga-sky/10">
              <Image
                src="https://images.unsplash.com/photo-1503454537195-1dcabb73ffb9?auto=format&fit=crop&w=900&q=80"
                alt="Child listening to a story"
                fill
                className="object-cover"
              />
            </div>
            <div className="mt-4 space-y-2 rounded-xl border border-slate-100 bg-white/90 p-4 shadow-inner">
              <p className="text-sm font-semibold text-saga-ink">Wake word</p>
              <div className="flex items-center justify-between text-sm">
                <span className="font-display text-lg text-saga-purple">“Hej Saga”</span>
                <span className="rounded-full bg-saga-sky/10 px-3 py-1 text-xs font-semibold text-saga-sky">
                  Live
                </span>
              </div>
              <p className="text-sm text-slate-600">
                Warm, gentle voice. Stories, weather, Q&A—always safe, always curious.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-6 pb-16 md:flex-row md:items-start">
        <div className="glass w-full rounded-3xl p-6 md:w-1/2">
          <div className="mb-3 inline-flex items-center gap-2 rounded-full bg-saga-purple/10 px-3 py-1 text-xs font-semibold text-saga-purple">
            Talk to me → full conversations
          </div>
          <h2 className="font-display text-3xl text-saga-ink">What&apos;s coming next</h2>
          <p className="mt-3 text-sm leading-relaxed text-slate-600">
            Today these toys echo you. Next build: they answer weather and time, tell cozy bedtime stories, and keep a gentle dialogue
            going in Swedish or English—all powered by a Rust backend and MySQL for parent controls.
          </p>
          <div className="mt-5 space-y-3">
            {upgrades.map((item) => (
              <div key={item.title} className="flex items-start gap-3 rounded-2xl border border-slate-100 bg-white/90 p-3">
                <div className="mt-0.5">{item.icon}</div>
                <div>
                  <p className="font-semibold text-saga-ink">{item.title}</p>
                  <p className="text-sm text-slate-600">{item.body}</p>
                </div>
              </div>
            ))}
          </div>
          <p className="mt-4 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
            Hosting on Vercel · DNS via Cloudflare · Live at sagatoy.com
          </p>
        </div>

        <div className="glass relative w-full rounded-3xl p-4 md:w-1/2">
          <div className="absolute right-4 top-4 rounded-full bg-saga-sky/10 px-3 py-1 text-xs font-semibold text-saga-sky">
            Prototype snapshot
          </div>
          <div className="relative aspect-[4/3] overflow-hidden rounded-2xl bg-gradient-to-br from-saga-purple/10 via-white to-saga-sky/10">
            <Image
              src="/talk-toys.svg"
              alt="Two talk-to-me toys prototype"
              fill
              className="object-contain p-6"
              priority
            />
          </div>
          <p className="mt-3 text-xs text-slate-500">
            Swap in your own photo by replacing <code className="rounded bg-slate-100 px-1">frontend/public/talk-toys.svg</code> with
            the real image from your LinkedIn post.
          </p>
        </div>
      </section>

      <section className="mx-auto grid w-full max-w-6xl gap-6 px-6 pb-16 md:grid-cols-3">
        {highlights.map((item) => (
          <div key={item.title} className="glass rounded-2xl p-6">
            <div className="mb-4 inline-flex rounded-full bg-saga-cloud px-3 py-2">{item.icon}</div>
            <h3 className="font-display text-xl text-saga-ink">{item.title}</h3>
            <p className="mt-2 text-sm leading-relaxed text-slate-600">{item.body}</p>
          </div>
        ))}
      </section>

      <section id="roadmap" className="mx-auto w-full max-w-6xl px-6 pb-20">
        <div className="glass rounded-3xl p-8">
          <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-saga-purple">Roadmap</p>
              <h2 className="font-display text-3xl text-saga-ink">Building in the open</h2>
            </div>
            <Link
              href="https://github.com/bluehawana/Sagatoy-AI-LLM-TTS-VPS"
              className="inline-flex items-center gap-2 text-sm font-semibold text-saga-purple"
            >
              View backend progress
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
          <div className="mt-6 grid gap-4 md:grid-cols-3">
            {roadmap.map((item) => (
              <div key={item.label} className="rounded-2xl border border-slate-100 bg-white/80 p-5">
                <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">{item.label}</p>
                <p className="mt-2 font-display text-lg text-saga-ink">{item.status}</p>
              </div>
            ))}
          </div>
          <div className="mt-6 flex flex-wrap gap-3 text-sm text-slate-600">
            <span className="rounded-full bg-saga-purple/10 px-3 py-1 text-saga-purple">Under construction</span>
            <span className="rounded-full bg-saga-gold/10 px-3 py-1 text-saga-gold">Designed for recruiters & partners</span>
            <span className="rounded-full bg-saga-sky/10 px-3 py-1 text-saga-sky">Hosting on Vercel + Cloudflare DNS</span>
          </div>
        </div>
      </section>

      <footer className="mx-auto flex w-full max-w-6xl flex-col gap-3 px-6 pb-12 text-sm text-slate-600 md:flex-row md:items-center md:justify-between">
        <p>© {new Date().getFullYear()} SagaToy — AI storytelling companion.</p>
        <div className="flex gap-4">
          <Link href="mailto:hello@sagatoy.com" className="hover:text-saga-purple">
            Contact
          </Link>
          <Link href="https://sagatoy.com" className="hover:text-saga-purple">
            sagatoy.com
          </Link>
        </div>
      </footer>
    </main>
  );
}
