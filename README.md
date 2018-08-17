# Python script to save json result from url to PostgreSQL database

## Example JSON

```buildoutcfg
{
  events: [
      {
        raw: "XX.XX.XX.XXX - beth [17/Aug/2018:13:31:18 +0000] "GET /page10.html HTTP/1.1" 200 643 "http://subdomain.domain.com/page7.html" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0"",
        logtypes: [
           "apache",
           "syslog"
        ],
        timestamp: 1534512678000,
        unparsed: null,
        logmsg: "XX.XX.XX.XXX - beth [17/Aug/2018:13:31:18 +0000] "GET /page10.html HTTP/1.1" 200 643 "http://subdomain.domain.com/page7.html" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0"",
        id: "d2ad5516-a221-11e8-800e-02ec14fc4836",
        tags: [
           "apache"
        ],
        event: {
          apache: {
             status: 200,
             timestamp: "17/Aug/2018:13:31:18 +0000",
             requestMethod: "GET",
             referer: "http://subdomain.domain.com/page7.html",
             remoteUser: "beth",
             requestURI: "/page10.html",
             userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0",
             requestProtocol: "HTTP/1.1",
             remoteAddr: "XX.XX.XX.XXX",
             size: 643
          },
          syslog: {
             severity: "Informational",
             appName: "apache-access",
             timestamp: "2018-08-17T13:31:18.662009+00:00",
             facility: "local use 0",
             priority: "134",
             host: "subdomain.domain.com"
          }
      }
  },
  {
        raw: "XX.XX.XX.XXX - john [17/Aug/2018:13:31:17 +0000] "GET /page7.html HTTP/1.1" 200 641 "http://subdomain.domain.com/page4.html" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0"",
        logtypes: [
           "apache",
           "syslog"
        ],
        timestamp: 1534512677000,
        unparsed: null,
        logmsg: "XX.XX.XX.XXX - john [17/Aug/2018:13:31:17 +0000] "GET /page7.html HTTP/1.1" 200 641 "http://subdomain.domain.com/page4.html" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0"",
        id: "d2ad4fd7-a221-11e8-80a7-02ec14fc4836",
        tags: [
           "apache"
        ],
        event: {
          apache: {
             status: 200,
             timestamp: "17/Aug/2018:13:31:17 +0000",
             requestMethod: "GET",
             referer: "http://subdomain.domain.com/page4.html",
             remoteUser: "john",
             requestURI: "/page7.html",
             userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0",
             requestProtocol: "HTTP/1.1",
             remoteAddr: "XX.XX.XX.XXX",
             size: 641
          },
          syslog: {
             severity: "Informational",
             appName: "apache-access",
             timestamp: "2018-08-17T13:31:18.662005+00:00",
             facility: "local use 0",
             priority: "134",
             host: "subdomain.domain.com"
          }
      }
  }
 ]
} 
```