// NOTIFY ME - Simple email subscription
// Stores in Cloudflare R2 and sends welcome email

export async function onRequestPost(context: any) {
  try {
    const formData = await context.request.formData();
    const email = formData.get("email");

    // Validate email
    if (!email || typeof email !== "string" || !email.includes("@")) {
      return new Response(
        JSON.stringify({
          error: "Invalid email address",
        }),
        {
          status: 400,
          headers: { "Content-Type": "application/json" },
        },
      );
    }

    const timestamp = new Date().toISOString();
    const referer = context.request.headers.get("referer") || "direct";
    const userAgent = context.request.headers.get("user-agent") || "unknown";

    // Create submission ID and data
    const submissionId = `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;

    const notifyData = {
      id: submissionId,
      email: email.toString(),
      timestamp: timestamp,
      source: referer.includes("info.sagatoy.com")
        ? "info.sagatoy.com"
        : "www.sagatoy.com",
      status: "subscribed",
      type: "notify_only",
      userAgent: userAgent,
    };

    console.log("New notify-me subscription:", notifyData);

    // Store in R2 bucket
    try {
      if (context.env.CONTACTS_BUCKET) {
        // Generate filename with date organization
        const date = new Date();
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");
        const filename = `notify/${year}/${month}/${day}/${submissionId}.json`;

        await context.env.CONTACTS_BUCKET.put(
          filename,
          JSON.stringify(notifyData, null, 2),
          {
            httpMetadata: {
              contentType: "application/json",
            },
          },
        );
        console.log("✅ Subscription saved to R2:", filename);
      } else {
        console.error("❌ CONTACTS_BUCKET binding is NOT available");
      }
    } catch (error: any) {
      console.error("Storage error:", error);
    }

    // Send welcome email FROM info@sagatoy.com TO customer
    try {
      const emailResponse = await fetch(
        "https://api.mailchannels.net/tx/v1/send",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            personalizations: [
              {
                to: [{ email: email.toString(), name: "Friend" }],
                dkim_domain: "sagatoy.com",
                dkim_selector: "mailchannels",
              },
            ],
            from: {
              email: "info@sagatoy.com",
              name: "Sagatoy Team",
            },
            subject: "Welcome to Sagatoy - Nordic AI Companion for Kids 🐬",
            content: [
              {
                type: "text/html",
                value: `
              <!DOCTYPE html>
              <html>
                <head>
                  <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 30px; border-radius: 10px 10px 0 0; text-align: center; }
                    .logo { font-size: 48px; margin-bottom: 10px; }
                    .content { background: #f9f9f9; padding: 40px 30px; border-radius: 0 0 10px 10px; }
                    .feature-box { background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0; }
                    .cta-button { background: #667eea; color: white; padding: 14px 32px; text-decoration: none; border-radius: 8px; display: inline-block; margin-top: 20px; font-weight: bold; }
                    .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #666; text-align: center; }
                  </style>
                </head>
                <body>
                  <div class="container">
                    <div class="header">
                      <div class="logo">🐬</div>
                      <h1 style="margin: 0; font-size: 32px;">Welcome to Sagatoy!</h1>
                      <p style="margin: 10px 0 0 0; font-size: 16px; opacity: 0.9;">Born in Gothenburg, Sweden 🇸🇪</p>
                    </div>
                    <div class="content">
                      <p style="font-size: 18px; color: #667eea; font-weight: bold;">Thank you for your interest in Sagatoy!</p>
                      <p>We're building the Nordic AI companion that helps children develop through natural conversation, multilingual learning, and screen-free play.</p>
                      <div class="feature-box">
                        <h3 style="margin-top: 0; color: #667eea;">🎯 What is Sagatoy?</h3>
                        <p>Sagatoy is an AI-powered companion toy designed with Nordic values.</p>
                      </div>
                      <div class="feature-box">
                        <h3 style="margin-top: 0; color: #667eea;">📅 Launch Timeline</h3>
                        <p><strong>Q2 2026</strong> - We'll notify you when we're ready to launch.</p>
                      </div>
                      <div style="text-align: center;">
                        <a href="https://www.sagatoy.com" class="cta-button">Visit Our Website</a>
                      </div>
                      <div class="footer">
                        <p><strong>Sagatoy AB</strong><br/>Gothenburg, Sweden 🇸🇪</p>
                      </div>
                    </div>
                  </div>
                </body>
              </html>
            `,
              },
            ],
          }),
        },
      );

      if (!emailResponse.ok) {
        const errorText = await emailResponse.text();
        console.error(
          "❌ MailChannels error:",
          emailResponse.status,
          errorText,
        );
      } else {
        console.log("✅ Welcome email sent successfully");
      }
    } catch (error: any) {
      console.error("❌ Email sending failed:", error);
    }

    return new Response(
      JSON.stringify({
        success: true,
        message:
          "Thank you! Check your inbox for a welcome email from Sagatoy.",
      }),
      {
        status: 200,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      },
    );
  } catch (error: any) {
    console.error("Notify subscription error:", error);
    return new Response(
      JSON.stringify({
        error: "Failed to process subscription",
        message: error?.message || "Unknown error",
      }),
      {
        status: 500,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      },
    );
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
}
