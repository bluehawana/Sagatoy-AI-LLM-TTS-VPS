// SUBSCRIBE - Dual purpose waitlist system
// Stores in Cloudflare R2 and sends notification to info@sagatoy.com

export async function onRequestPost(context: any) {
  try {
    const formData = await context.request.formData();
    const email = formData.get("email");

    if (!email || typeof email !== "string" || !email.includes("@")) {
      return new Response(JSON.stringify({ error: "Invalid email address" }), {
        status: 400,
        headers: { "Content-Type": "application/json" },
      });
    }

    const timestamp = new Date().toISOString();
    const userAgent = context.request.headers.get("user-agent") || "unknown";
    const referer = context.request.headers.get("referer") || "direct";

    // Create submission ID
    const submissionId = `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;

    const customerData = {
      id: submissionId,
      email: email.toString(),
      timestamp: timestamp,
      source: referer.includes("info.sagatoy.com")
        ? "info.sagatoy.com"
        : "www.sagatoy.com",
      userAgent: userAgent,
      status: "pending",
      type: "subscribe",
    };

    console.log("New subscribe signup:", customerData);

    // Store in R2 bucket
    try {
      if (context.env.CONTACTS_BUCKET) {
        // Generate filename with date organization
        const date = new Date();
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");
        const filename = `subscribe/${year}/${month}/${day}/${submissionId}.json`;

        await context.env.CONTACTS_BUCKET.put(
          filename,
          JSON.stringify(customerData, null, 2),
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
    } catch (storageError: any) {
      console.error("Storage error:", storageError);
    }

    // Send admin notification email to info@sagatoy.com
    try {
      const mailResponse = await fetch(
        "https://api.mailchannels.net/tx/v1/send",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            personalizations: [
              {
                to: [{ email: "info@sagatoy.com", name: "Sagatoy Team" }],
                dkim_domain: "sagatoy.com",
                dkim_selector: "mailchannels",
              },
            ],
            from: {
              email: "waitlist@sagatoy.com",
              name: "Sagatoy Waitlist Bot",
            },
            subject: `🎉 New Waitlist Signup: ${email}`,
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
                      .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; }
                      .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                      .email-box { background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0; }
                      .footer { margin-top: 20px; font-size: 12px; color: #666; }
                    </style>
                  </head>
                  <body>
                    <div class="container">
                      <div class="header">
                        <h1>🚀 New Waitlist Signup!</h1>
                      </div>
                      <div class="content">
                        <p><strong>Great news!</strong> A potential customer just joined your Sagatoy waitlist.</p>
                        <div class="email-box">
                          <p><strong>📧 Email:</strong> ${email}</p>
                          <p><strong>🕒 Timestamp:</strong> ${timestamp}</p>
                          <p><strong>🌐 Source:</strong> ${customerData.source}</p>
                          <p><strong>📊 Status:</strong> Pending contact</p>
                        </div>
                        <h3>Next Steps:</h3>
                        <ul>
                          <li>✅ Customer added to R2 storage</li>
                          <li>📧 Email saved for marketing campaign</li>
                        </ul>
                        <div class="footer">
                          <p>Born in Gothenburg, Sweden 🇸🇪</p>
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

      if (!mailResponse.ok) {
        const errorText = await mailResponse.text();
        console.error("MailChannels error:", errorText);
      } else {
        console.log("✅ Admin notification sent to info@sagatoy.com");
      }
    } catch (emailError: any) {
      console.error("Email notification failed:", emailError);
    }

    return new Response(
      JSON.stringify({
        success: true,
        message:
          "Thank you for joining our waitlist! We'll notify you when we launch in Q2 2026.",
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
    console.error("Subscription error:", error);
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

// CORS preflight
export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
}
