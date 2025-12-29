// Cloudflare Pages Function to handle email subscriptions
interface Env {
  WAITLIST?: KVNamespace;
}

export async function onRequestPost(context: { request: Request; env: Env }) {
  try {
    const formData = await context.request.formData();
    const email = formData.get('email');

    if (!email || typeof email !== 'string' || !email.includes('@')) {
      return new Response(JSON.stringify({ error: 'Invalid email address' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Simple email notification using fetch to a webhook or service
    // For now, we'll just return success and log the email
    // You can set up email forwarding in Cloudflare later

    const emailData = {
      email: email,
      timestamp: new Date().toISOString(),
      source: 'waitlist'
    };

    console.log('New waitlist signup:', emailData);

    // Try to store in KV if available (optional)
    try {
      if (context.env.WAITLIST) {
        await context.env.WAITLIST.put(
          `signup:${email}`,
          JSON.stringify(emailData)
        );
      }
    } catch (kvError) {
      console.log('KV storage not available, skipping storage');
    }

    // Send notification email using Resend API (if you add RESEND_API_KEY to env)
    // Or use any other email service you prefer
    const RESEND_API_KEY = context.env?.RESEND_API_KEY;

    if (RESEND_API_KEY) {
      try {
        await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${RESEND_API_KEY}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            from: 'waitlist@sagatoy.com',
            to: 'info@sagatoy.com',
            subject: `New Waitlist Signup: ${email}`,
            html: `<p><strong>New waitlist signup!</strong></p><p>Email: ${email}</p><p>Timestamp: ${emailData.timestamp}</p>`
          }),
        });
      } catch (emailError) {
        console.error('Email send failed:', emailError);
        // Continue anyway - we still want to save the signup
      }
    }

    return new Response(JSON.stringify({
      success: true,
      message: 'Thank you for joining our waitlist!'
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
      message: error?.message || 'Unknown error',
      details: error?.stack || ''
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
