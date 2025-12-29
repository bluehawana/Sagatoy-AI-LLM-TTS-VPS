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
      source: 'waitlist'
    };

    console.log('New waitlist signup:', emailData);

    // Send notification email using Resend API
    const RESEND_API_KEY = context.env?.RESEND_API_KEY;

    if (RESEND_API_KEY) {
      try {
        const emailResponse = await fetch('https://api.resend.com/emails', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${RESEND_API_KEY}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            from: 'Sagatoy Waitlist <waitlist@sagatoy.com>',
            to: ['info@sagatoy.com'],
            subject: `New Waitlist Signup: ${email}`,
            html: `
              <h2>New Waitlist Signup!</h2>
              <p><strong>Email:</strong> ${email}</p>
              <p><strong>Timestamp:</strong> ${emailData.timestamp}</p>
              <p><strong>Source:</strong> www.sagatoy.com waitlist form</p>
            `
          }),
        });

        if (!emailResponse.ok) {
          console.error('Resend API error:', await emailResponse.text());
        }
      } catch (emailError: any) {
        console.error('Email send failed:', emailError);
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
