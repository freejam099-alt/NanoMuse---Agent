package io.github.nanomuse.ui.muse

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.snap
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.openminis.app.R
import com.openminis.app.ui.chat.animationsDisabled
import io.github.nanomuse.ui.home.MuseTones

/**
 * Reusable decorative app mark: Hugeicons AI Brain 02, free Stroke Rounded, on the blue brand gradient.
 * [motionActive] plays one short sheen when the mark becomes active; system animation settings are respected.
 */
@Composable
fun NmBrandMark(
    size: Dp = 104.dp,
    modifier: Modifier = Modifier,
    motionActive: Boolean = false,
) {
    val context = LocalContext.current
    val motionDisabled = remember(context) { animationsDisabled(context) }
    val sheenProgress by animateFloatAsState(
        targetValue = if (motionActive && !motionDisabled) 1f else 0f,
        animationSpec = if (motionDisabled) snap() else tween(durationMillis = 600, easing = LinearEasing),
        label = "nmBrandMarkSheen",
    )
    val shape = RoundedCornerShape(size * 0.24f)

    Box(
        modifier = modifier
            .size(size)
            .clip(shape)
            .drawBehind {
                drawRect(MuseTones.brandGradient)
                if (motionActive && !motionDisabled && sheenProgress < 1f) {
                    val centerX = this.size.width * (2f * sheenProgress - 0.8f)
                    drawRect(
                        brush = androidx.compose.ui.graphics.Brush.linearGradient(
                            colors = listOf(
                                Color.Transparent,
                                Color.White.copy(alpha = 0.20f),
                                Color.Transparent,
                            ),
                            start = Offset(centerX - this.size.width * 0.30f, 0f),
                            end = Offset(centerX + this.size.width * 0.30f, this.size.height),
                        ),
                    )
                }
            },
        contentAlignment = Alignment.Center,
    ) {
        Icon(
            painter = painterResource(R.drawable.ic_stat_nanomuse),
            contentDescription = null,
            tint = MuseTones.actionForeground,
            modifier = Modifier.size(size * 0.58f),
        )
    }
}
