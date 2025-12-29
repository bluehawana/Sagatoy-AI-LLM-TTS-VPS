// Cloudflare Pages Function to handle email subscriptions
export async function onRequestPost(context) {
  try {
    const formData = await context.request.formData();
    const email = formData.get('email');

    if (!email || !email.includes('@')) {
      return new Response(JSON.stringify({ error: 'Invalid email address' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Send email using Cloudflare's Email Routing or MailChannels
    // For now, we'll use MailChannels (free for Cloudflare Workers)
    const emailContent = {
      personalizations: [{
        to: [{ email: 'info@sagatoy.com', name: 'Sagatoy Team' }],
      }],
      from: {
        email: 'notifications@sagatoy.com',
        name: 'Sagatoy Waitlist'
      },
      subject: `New Waitlist Signup: ${email}`,
      content: [{
        type: 'text/plain',
        value: `New user signed up for the waitlist!\n\nEmail: ${email}\n\nTimestamp: ${new Date().toISOString()}`
      }]
    };

    // Send via MailChannels API
    const mailResponse = await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(emailContent),
    });

    if (!mailResponse.ok) {
      console.error('MailChannels error:', await mailResponse.text());
      throw new Error('Failed to send notification email');
    }

    // Store in KV storage if needed (optional)
    // await context.env.WAITLIST.put(email, JSON.stringify({ timestamp: Date.now() }));

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

  } catch (error) {
    console.error('Subscription error:', error);
    return new Response(JSON.stringify({
      error: 'Failed to process subscription',
      message: error.message
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
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
