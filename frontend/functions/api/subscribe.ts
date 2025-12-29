// Cloudflare Pages Function to handle email subscriptions
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

    const emailData = {
      email: email,
      timestamp: new Date().toISOString(),
      source: 'waitlist',
      userAgent: context.request.headers.get('user-agent') || 'unknown'
    };

    console.log('New waitlist signup:', emailData);

    // Send email using MailChannels (free for Cloudflare Workers)
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
                    </style>
                  </head>
                  <body>
                    <div class="container">
                      <div class="header">
                        <h1>🚀 New Waitlist Signup!</h1>
                      </div>
                      <div class="content">
                        <p><strong>Great news!</strong> Someone just joined your Sagatoy waitlist.</p>

                        <div class="email-box">
                          <p><strong>📧 Email:</strong> ${email}</p>
                          <p><strong>🕒 Timestamp:</strong> ${emailData.timestamp}</p>
                          <p><strong>🌐 Source:</strong> ${emailData.source === 'waitlist' ? 'www.sagatoy.com' : 'info.sagatoy.com'}</p>
                          <p><strong>💻 User Agent:</strong> ${emailData.userAgent}</p>
                        </div>

                        <p>This is your <strong>first potential customer!</strong> 🎯</p>

                        <p>Make sure to save this email to your customer database and reach out when you launch in Q2 2026.</p>

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
        throw new Error('Failed to send email notification');
      }

      console.log('Email sent successfully to info@sagatoy.com');

    } catch (emailError: any) {
      console.error('Email send failed:', emailError);
      // Don't fail the whole request if email fails
      // Still return success to user
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

// Handle CORS preflight
export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    }
  });
}
