import { CallHandler, ExecutionContext, Injectable, NestInterceptor, TooManyRequestsException } from '@nestjs/common'
import { Observable } from 'rxjs'

interface RequestTracker {
  count: number
  resetTime: number
}

@Injectable()
export class RateLimitInterceptor implements NestInterceptor {
  private requests: Map<string, RequestTracker> = new Map()
  private readonly maxRequests = parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || '100', 10)
  private readonly windowMs = parseInt(process.env.RATE_LIMIT_WINDOW_MS || '60000', 10) // 1 minute default

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest()
    const response = context.switchToHttp().getResponse()

    // Get client IP
    const clientIp =
      request.ip ||
      request.connection.remoteAddress ||
      request.headers['x-forwarded-for'] ||
      'unknown'

    const key = `${clientIp}-${request.path}`
    const now = Date.now()

    // Get or create request tracker
    let tracker = this.requests.get(key)

    if (!tracker || now > tracker.resetTime) {
      // Reset tracker
      tracker = {
        count: 1,
        resetTime: now + this.windowMs,
      }
    } else {
      tracker.count++
    }

    // Update tracker
    this.requests.set(key, tracker)

    // Set rate limit headers
    response.setHeader('X-RateLimit-Limit', this.maxRequests)
    response.setHeader('X-RateLimit-Remaining', Math.max(0, this.maxRequests - tracker.count))
    response.setHeader('X-RateLimit-Reset', new Date(tracker.resetTime).toISOString())

    // Check rate limit
    if (tracker.count > this.maxRequests) {
      throw new TooManyRequestsException(
        `Rate limit exceeded. Max ${this.maxRequests} requests per ${this.windowMs}ms`,
      )
    }

    return next.handle()
  }
}
