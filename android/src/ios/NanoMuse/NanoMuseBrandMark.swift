//
//  NanoMuseBrandMark.swift
//  nanoMuse
//
//  The app identity mark for sign-in and permission screens. The shared
//  NanoMuseBrandMark image set is generated from assets/brand/nanomuse-mark.svg;
//  it depicts Hugeicons AI Brain 02 in free Stroke Rounded style. The dragon
//  remains the agent's face and is not used here.
//

import SwiftUI

/// Shared app identity icon, rendered from the generated NanoMuseBrandMark asset set.
struct NanoMuseBrandMark: View {
    var size: CGFloat = 72

    var body: some View {
        Image("NanoMuseBrandMark")
            .resizable()
            .interpolation(.high)
            .scaledToFit()
            .frame(width: size, height: size)
            .accessibilityHidden(true)
    }
}
