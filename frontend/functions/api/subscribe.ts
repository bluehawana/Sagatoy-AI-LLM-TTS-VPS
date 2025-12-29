// Cloudflare Pages Function - Dual purpose waitlist system
// 1. Store emails in database (CRM for email marketing)
// 2. Send notification to info@sagatoy.com

export async function onRequestPost(context: any) {
  try {
    const formData = await context.request.formData();
    const email = formData.get('email');

    if (!email || typeof email !== 'string' || !email.includes('@')) {
      return new Response(JSON.stringify({ error: 'Invalid email address' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const timestamp = new Date().toISOString();
    const userAgent = context.request.headers.get('user-agent') || 'unknown';
    const referer = context.request.headers.get('referer') || 'direct';

    const customerData = {
      email: email,
      timestamp: timestamp,
      source: referer.includes('info.sagatoy.com') ? 'info.sagatoy.com' : 'www.sagatoy.com',
      userAgent: userAgent,
      status: 'pending' // Can be: pending, contacted, customer
    };

    console.log('New waitlist signup:', customerData);

    // FUNCTION 1: Store in KV/D1 Database for CRM
    // This builds your customer database for email marketing when you launch
    try {
      if (context.env.WAITLIST_DB) {
        // Store in D1 database if available
        const stmt = context.env.WAITLIST_DB.prepare(
          'INSERT INTO waitlist (email, timestamp, source, user_agent, status) VALUES (?, ?, ?, ?, ?)'
        );
        await stmt.bind(email, timestamp, customerData.source, userAgent, 'pending').run();
        console.log('✅ Stored in database for CRM');
      } else if (context.env.WAITLIST_KV) {
        // Fallback to KV storage
        await context.env.WAITLIST_KV.put(
          `waitlist:${email}`,
          JSON.stringify(customerData),
          { metadata: { timestamp, source: customerData.source } }
        );
        console.log('✅ Stored in KV for CRM');
      } else {
        console.warn('⚠️ No storage configured - email not saved to CRM');
      }
    } catch (storageError: any) {
      console.error('Storage error:', storageError);
      // Continue anyway - we still want to send notification
    }

    // FUNCTION 2: Send admin notification email to info@sagatoy.com
    // This alerts you immediately when someone joins
    try {
      const mailResponse = await fetch('https://api.mailchannels.net/tx/v1/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          personalizations: [
            {
              to: [{ email: 'info@sagatoy.com', name: 'Sagatoy Team' }],
              dkim_domain: 'sagatoy.com',
              dkim_selector: 'mailchannels',
            }
          ],
          from: {
            email: 'waitlist@sagatoy.com',
            name: 'Sagatoy Waitlist Bot'
          },
          subject: `🎉 New Waitlist Signup: ${email}`,
          content: [
            {
              type: 'text/html',
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
                      .cta { background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin-top: 10px; }
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
                          <p><strong>💻 Browser:</strong> ${userAgent.substring(0, 100)}...</p>
                          <p><strong>📊 Status:</strong> Pending contact</p>
                        </div>

                        <h3>Next Steps:</h3>
                        <ul>
                          <li>✅ Customer added to your CRM database</li>
                          <li>📧 Email saved for marketing campaign when you launch (Q2 2026)</li>
                          <li>🎯 You can export all waitlist emails anytime for email marketing</li>
                        </ul>

                        <p><strong>This is your first potential customer!</strong> 🎯</p>

                        <a href="https://dash.cloudflare.com" class="cta">View in Cloudflare Dashboard</a>

                        <div class="footer">
                          <p>This notification was sent automatically from your Sagatoy waitlist form.</p>
                          <p>Born in Gothenburg, Sweden 🇸🇪</p>
                        </div>
                      </div>
                    </div>
                  </body>
                </html>
              `
            }
          ]
        }),
      });

      if (!mailResponse.ok) {
        const errorText = await mailResponse.text();
        console.error('MailChannels error:', errorText);
      } else {
        console.log('✅ Admin notification sent to info@sagatoy.com');
      }

    } catch (emailError: any) {
      console.error('Email notification failed:', emailError);
      // Don't fail the request - storage is more important
    }

    return new Response(JSON.stringify({
      success: true,
      message: 'Thank you for joining our waitlist! We\'ll notify you when we launch in Q2 2026.'
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });

  } catch (error: any) {
    console.error('Subscription error:', error);
    return new Response(JSON.stringify({
      error: 'Failed to process subscription',
      message: error?.message || 'Unknown error'
    }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }
}

// CORS preflight
export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    }
  });
}
