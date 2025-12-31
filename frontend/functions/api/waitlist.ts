// JOIN WAITLIST - Full CRM form (First name, Last name, Phone, Email, etc.)
// Stores complete customer information for serious leads

export async function onRequestPost(context: any) {
  try {
    const formData = await context.request.formData();

    const firstName = formData.get('firstName');
    const lastName = formData.get('lastName');
    const email = formData.get('email');
    const phone = formData.get('phone');
    const country = formData.get('country') || '';
    const interests = formData.get('interests') || '';

    // Validate required fields
    if (!firstName || !lastName || !email || !phone) {
      return new Response(JSON.stringify({
        error: 'Please fill in all required fields'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    if (!email.toString().includes('@')) {
      return new Response(JSON.stringify({
        error: 'Invalid email address'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const timestamp = new Date().toISOString();
    const referer = context.request.headers.get('referer') || 'direct';

    const customerData = {
      firstName: firstName.toString(),
      lastName: lastName.toString(),
      email: email.toString(),
      phone: phone.toString(),
      country: country.toString(),
      interests: interests.toString(),
      timestamp: timestamp,
      source: referer.includes('info.sagatoy.com') ? 'info.sagatoy.com' : 'www.sagatoy.com',
      status: 'waitlist', // waitlist, contacted, customer
      type: 'full_lead' // Full CRM lead with complete info
    };

    console.log('New waitlist signup (FULL CRM):', customerData);

    // Store in KV/D1 database for CRM
    try {
      if (context.env.WAITLIST_KV) {
        await context.env.WAITLIST_KV.put(
          `waitlist:${email}`,
          JSON.stringify(customerData),
          {
            metadata: {
              timestamp,
              type: 'full_lead',
              name: `${firstName} ${lastName}`
            }
          }
        );
        console.log('✅ Full customer data stored in CRM');
      }
    } catch (error: any) {
      console.error('Storage error:', error);
    }

    // Send admin notification to info@sagatoy.com
    try {
      const emailResponse = await fetch('https://api.mailchannels.net/tx/v1/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          personalizations: [{
            to: [{ email: 'info@sagatoy.com', name: 'Sagatoy Team' }],
            dkim_domain: 'sagatoy.com',
            dkim_selector: 'mailchannels',
          }],
          from: {
            email: 'waitlist@sagatoy.com',
            name: 'Sagatoy Waitlist CRM'
          },
          subject: `🎯 New FULL Waitlist Lead: ${firstName} ${lastName}`,
          content: [{
            type: 'text/html',
            value: `
              <!DOCTYPE html>
              <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                  <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0;">
                      <h1>🎯 New FULL Waitlist Lead!</h1>
                    </div>
                    <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                      <p><strong>High-quality lead with complete information!</strong></p>

                      <div style="background: white; padding: 20px; border-left: 4px solid #667eea; margin: 20px 0;">
                        <h3>Customer Details:</h3>
                        <p><strong>👤 Name:</strong> ${firstName} ${lastName}</p>
                        <p><strong>📧 Email:</strong> ${email}</p>
                        <p><strong>📱 Phone:</strong> ${phone}</p>
                        ${country ? `<p><strong>🌍 Country:</strong> ${country}</p>` : ''}
                        ${interests ? `<p><strong>💡 Interests:</strong> ${interests}</p>` : ''}
                        <p><strong>🕒 Timestamp:</strong> ${timestamp}</p>
                        <p><strong>🌐 Source:</strong> ${customerData.source}</p>
                      </div>

                      <h3>Next Steps:</h3>
                      <ul>
                        <li>✅ Full customer profile saved to CRM</li>
                        <li>📞 Contact within 24-48 hours</li>
                        <li>🎯 High-intent customer - prioritize!</li>
                      </ul>

                      <p style="margin-top: 20px; font-size: 12px; color: #666;">
                        This is a FULL LEAD - they provided complete contact information.
                        <br/>Born in Gothenburg, Sweden 🇸🇪
                      </p>
                    </div>
                  </div>
                </body>
              </html>
            `
          }]
        }),
      });

      if (!emailResponse.ok) {
        const errorText = await emailResponse.text();
        console.error('❌ MailChannels error:', emailResponse.status, errorText);
      } else {
        console.log('✅ Admin notification sent successfully');
      }
    } catch (error: any) {
      console.error('❌ Email failed:', error);
    }

    return new Response(JSON.stringify({
      success: true,
      message: `Thank you ${firstName}! You're on our waitlist. We'll contact you before launch in Q2 2026.`
    }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });

  } catch (error: any) {
    console.error('Waitlist error:', error);
    return new Response(JSON.stringify({
      error: 'Failed to join waitlist',
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

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    }
  });
}
